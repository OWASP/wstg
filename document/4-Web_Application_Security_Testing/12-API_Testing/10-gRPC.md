# gRPC

|ID          |
|------------|
|WSTG-APIT-10|

## Summary

[gRPC](https://grpc.io/) is a remote procedure call framework that runs over HTTP/2. Services and their messages are defined in `.proto` files and encoded as Protocol Buffers (protobuf), a compact binary format. Each method is called with a POST request to a path of the form `/<package>.<Service>/<Method>`, with a `content-type` of `application/grpc`. The [gRPC over HTTP/2 protocol description](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) covers the framing and headers.

Browsers cannot send native gRPC requests, so browser clients use [gRPC-Web](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md), often through a proxy such as Envoy that translates to gRPC. gRPC-Web works over HTTP/1.1 and uses the `application/grpc-web` content type, or `application/grpc-web-text` for a base64-encoded body.

gRPC APIs are exposed to the same flaws as other APIs, such as broken object and function level authorization and injection. What changes is how a tester finds the methods, builds requests, and reads responses, and a few weaknesses that come from the framework itself:

- The binary format makes requests hard to read and edit in an intercepting proxy, so gRPC services often get less testing than REST endpoints.
- Server reflection and other built-in services can describe or expose more than intended.
- Authentication and authorization are usually added through interceptors, which can be applied to some methods or call types and not others.
- The same service is often exposed on more than one path, such as native gRPC, gRPC-Web and a REST gateway, each with its own controls.

This page covers what is specific to gRPC. For the general API tests, see [API Testing Overview](00-API_Testing_Overview.md) and the other pages in this section.

## Test Objectives

- Identify gRPC and gRPC-Web endpoints and recover the service definitions.
- Determine whether reflection and built-in services expose information that should not be public.
- Assess whether authentication and authorization are enforced for every method, call type and entry point.
- Assess how the service handles unexpected message content, sizes and errors.

## How to Test

### Identify gRPC Endpoints

Look for the following when mapping the application, as described in [API Reconnaissance](01-API_Reconnaissance.md):

- Requests with a `content-type` of `application/grpc`, `application/grpc-web` or `application/grpc-web-text`, and responses with `grpc-status` and `grpc-message` headers or trailers.
- POST requests to paths such as `/shop.v1.OrderService/GetOrder`.
- Generated gRPC-Web client code in the JavaScript bundles. It contains the service and method paths, and often the message field names and numbers.
- Ports that accept HTTP/2 without TLS (h2c). These may be internal ports that are reachable from outside.

### Recover the Service Definitions

Check whether the server supports [server reflection](https://grpc.io/docs/guides/reflection/). With reflection, a client can list every service and describe its methods and messages. [grpcurl](https://github.com/fullstorydev/grpcurl) can query it:

```bash
grpcurl api.example.com:443 list
grpcurl api.example.com:443 describe shop.v1.OrderService
grpcurl -plaintext internal.example.com:50051 list
```

Reflection in production is not a vulnerability by itself, but it gives an attacker the complete API, including methods that the client never calls. Note any services or methods that look internal, such as admin, debug or migration methods.

If reflection is disabled, recover the definitions from other sources:

- `.proto` files or generated code in the web client, mobile applications, public repositories and SDKs.
- Decoding captured messages without a schema. The [Blackbox Protobuf](https://github.com/nccgroup/blackboxprotobuf) extension for Burp Suite decodes and edits protobuf messages, and infers field types from the encoded data.

### Test Built-in Services

gRPC servers often register standard services next to the application's own. Check whether these are reachable from outside and what they reveal:

- The reflection service (`grpc.reflection.v1.ServerReflection` and the older `grpc.reflection.v1alpha.ServerReflection`).
- The [health checking service](https://grpc.io/docs/guides/health-checking/) (`grpc.health.v1.Health`), which can reveal the names of internal services.
- Channelz (`grpc.channelz.v1.Channelz`), a debugging service that reports internal channels, connections and peer addresses.

### Test Authentication and Authorization

gRPC sends credentials as request metadata, which is carried in HTTP/2 headers, for example `authorization: Bearer <token>`. The [authentication guide](https://grpc.io/docs/guides/auth/) describes the supported mechanisms. Test every method found in the previous steps, not only the ones the client uses:

- Call each method without credentials, with an expired token and with a token of a low-privileged user.
- Test all four call types: unary, server streaming, client streaming and bidirectional streaming. In several gRPC libraries, interceptors for unary and streaming calls are registered separately, and a server that only adds an authentication interceptor for unary calls leaves its streaming methods open.
- For long-lived streams, check whether the server notices when the token expires or the user's access is removed during the stream.
- Change object identifiers in the request messages to test object level authorization, as described in [API Broken Object Level Authorization](02-API_Broken_Object_Level_Authorization.md). Call internal or admin methods as a normal user, as described in [API Broken Function Level Authorization](04-API_Broken_Function_Level_Authorization.md).

### Test Every Entry Point

A gRPC service is often published in more than one way:

- Native gRPC, usually on its own port.
- gRPC-Web through a proxy.
- A REST and JSON interface generated from `google.api.http` annotations by a transcoding gateway, such as [grpc-gateway](https://github.com/grpc-ecosystem/grpc-gateway), Envoy or a cloud API gateway. See [HTTP to gRPC transcoding](https://cloud.google.com/endpoints/docs/grpc/transcoding).

Authentication, authorization, rate limiting and input checks are sometimes enforced only in the proxy or gateway. Repeat the authorization tests on each entry point that can be reached, and in particular check whether the native gRPC port can be reached directly, bypassing the gateway.

### Test Message Handling

Protobuf messages behave differently from JSON, which affects how the server validates them:

- **Unused fields:** a request message can define fields that the client never sets, such as `role`, `owner_id` or `price`. Set them and check whether the server applies them, as described in [Mass Assignment](../07-Injection/20-Mass_Assignment.md). For update methods that take a `google.protobuf.FieldMask`, add protected fields to the mask.
- **Default values:** in proto3, a scalar field that is not sent has its default value, such as `0`, `false` or an empty string, and the server cannot tell it apart from a field that was sent with that value. See the [proto3 language guide](https://protobuf.dev/programming-guides/proto3/). Check how the server treats missing fields, zero amounts and empty identifiers.
- **Unexpected values:** send negative numbers to signed integer fields, very large values, and enum values that are not defined. Protobuf accepts unknown enum values in proto3, so the application must check them.
- **Injection:** string and bytes fields reach databases, shells and templates like any other input. Run the usual injection tests, such as [SQL Injection](../07-Injection/05-SQL_Injection.md), through the message fields.

Tools that can build and send gRPC requests from the service definitions include grpcurl, [grpcui](https://github.com/fullstorydev/grpcui), the [ZAP gRPC add-on](https://www.zaproxy.org/docs/desktop/addons/grpc-support/), and Burp Suite with a protobuf extension.

### Test Errors and Limits

- Check the `grpc-message` and `grpc-status-details-bin` values in error responses. The details can contain [rich error models](https://grpc.io/docs/guides/error/) such as `google.rpc.DebugInfo`, which may include stack traces. See [Improper Error Handling](../08-Error_Handling/01-Improper_Error_Handling.md).
- Compare the [status codes](https://grpc.io/docs/guides/status-codes/) for existing and non-existing objects, for example `NOT_FOUND` against `PERMISSION_DENIED`, which can reveal which objects exist.
- Send messages larger than expected, and many messages on one stream. Check whether the server limits the message size, the number of messages and concurrent streams, and the duration of a call, and whether a client that sets no [deadline](https://grpc.io/docs/guides/deadlines/) can hold server resources.
- If the server accepts [compressed messages](https://grpc.io/docs/guides/compression/) (the `grpc-encoding` header), check whether the size limit is applied after decompression.

## Remediation

- Disable server reflection, channelz and other debugging services on externally reachable servers, or restrict them to authenticated administrators.
- Enforce authentication and authorization for every method and call type, using interceptors for both unary and streaming calls, and check authorization on each object a request refers to.
- Apply the same controls on every entry point, and do not expose the native gRPC port when clients are meant to go through a gateway.
- Validate every field on the server, including enum values, ranges and fields that the client is not expected to set. Use separate request messages, or field masks with an allow list, for fields users may change.
- Set limits for message size, streams and call duration, and return generic error details to clients.
- Use TLS for all external gRPC traffic.

## Tools

- [grpcurl](https://github.com/fullstorydev/grpcurl)
- [grpcui](https://github.com/fullstorydev/grpcui)
- [ZAP](https://www.zaproxy.org/) with the [gRPC add-on](https://www.zaproxy.org/docs/desktop/addons/grpc-support/)
- [Burp Suite](https://portswigger.net/burp) with the [Blackbox Protobuf](https://github.com/nccgroup/blackboxprotobuf) extension

## References

- [gRPC: Documentation](https://grpc.io/docs/)
- [gRPC over HTTP/2](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md)
- [gRPC-Web protocol](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md)
- [gRPC: Authentication](https://grpc.io/docs/guides/auth/)
- [Protocol Buffers: Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
