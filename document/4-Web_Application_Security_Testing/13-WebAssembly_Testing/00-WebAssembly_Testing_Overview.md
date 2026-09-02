# WebAssembly Testing Overview

## WebAssembly Introduction

WebAssembly (abbreviated *Wasm*) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications. It provides a way to run code written in multiple languages—such as C, C++, Rust, and Go—on the web at near-native speeds.

The adoption of WebAssembly has been driven by the need for high performance in web applications (e.g., video editing, gaming engines, cryptographic libraries) and the desire to port legacy desktop applications to the web without rewriting them in JavaScript.

As with the introduction of any new architecture, WebAssembly carries unique flaws and vulnerabilities. While the Wasm virtual machine is sandboxed from the host environment, the code executing *inside* the Wasm module retains the memory-safety vulnerabilities inherent to the source language. Furthermore, the boundary between the host and the Wasm module can provide an unrestricted path to application compromise if not secured properly.

This chapter attempts to guide the security researcher in the concepts necessary for testing WebAssembly applications, investigating its core technologies, execution environments, and vulnerability paradigms.

## History

Due to its performance benefits, WebAssembly has rapidly evolved from a browser-specific feature to a versatile technology running across servers, edge networks, and embedded devices.

WebAssembly was first announced in 2015 as a joint effort by engineers from Mozilla, Google, Microsoft, and Apple. By 2017, the Minimum Viable Product (MVP) was released and shipped by all major browser engines, establishing Wasm as the fourth language to run natively in browsers (alongside HTML, CSS, and JavaScript).

In December 2019, the World Wide Web Consortium (W3C) published the WebAssembly Core Specification as an official web standard. Around the same time, the WebAssembly System Interface (WASI) was introduced. WASI standardized how WebAssembly modules interact with operating systems, propelling Wasm outside the browser into backend services, microservices, and serverless edge computing platforms (like Cloudflare Workers and Fastly Compute).

## Which WebAssembly Environment?

Before making assumptions about the attack surface, it is helpful to be aware of the environment in which the WebAssembly module operates. The security researcher may encounter:

- **Client-Side (Browser) Wasm:** The `.wasm` file is downloaded and executed by the user's browser. It relies on JavaScript "glue code" to interact with the DOM and Web APIs.
- **Server-Side:** The Wasm module runs on the backend, processing API requests or performing heavy computations. Vulnerabilities here can lead directly to server compromise.
- **Serverless / Edge Computing:** Wasm instances are spun up on edge nodes to intercept and process HTTP requests. These environments often reuse memory instances to reduce latency, introducing cross-tenant state leakage risks.
- **Standalone WASI:** The module runs natively on the OS via runtimes like Wasmtime or Wasmer, governed by a capability-based security model.

## WebAssembly Core Components

WebAssembly architecture relies on several fundamental concepts. Understanding these is crucial for analyzing how vulnerabilities manifest.

### Modules

A WebAssembly Module is a compiled `.wasm` binary file. It is stateless and contains the compiled bytecode, type signatures, and data segments. In text format, it is represented as WebAssembly Text Format (WAT).

### Linear Memory

Unlike native applications that utilize OS-managed heaps and stacks, a WebAssembly instance stores its runtime data inside a single, contiguous byte array called **Linear Memory**. This memory is exposed to the host as an `ArrayBuffer`. The Wasm module's stack, heap, string literals, and global variables all share this unmanaged, flat memory space.

### Tables

A Table is an array of opaque values, typically function references. Because WebAssembly enforces Control-Flow Integrity (CFI) and does not allow direct code execution from Linear Memory, source-level function pointers (such as in C, C++, or Rust) and dynamic call targets are compiled into integer indices pointing to specific slots in a Table. Indirect calls (call_indirect) are subsequently executed using these indices.

### Imports and Exports

WebAssembly cannot interact with the outside world autonomously.

- **Imports:** Functions or variables provided by the host (e.g., a JS function like `console.log`) that the Wasm module can call.
- **Exports:** Functions or memory instances inside the Wasm module that are made accessible to the host.

## The Security Paradigm

WebAssembly is inherently sandboxed; a module cannot escape its virtual machine to read arbitrary files or network sockets without the host explicitly importing those capabilities.

However, **internal memory safety is not guaranteed.** When legacy C/C++ code is compiled to WebAssembly, standard binary mitigations are lost:

- **No ASLR (Address Space Layout Randomization):** Memory offsets are predictable.
- **No Default Stack Protectors:** Stack frames lack canaries.
- **No W^X (Write XOR Execute) isolation:** Control flow data (like table indices) and variables reside alongside user input buffers.

Consequently, classic memory corruption vulnerabilities (Buffer Overflows, Use-After-Free, Format Strings) survive compilation. An attacker can overwrite adjacent data in Linear Memory to manipulate application logic, alter indirect call table indices (ret2win), or corrupt output buffers consumed by the host, translating a Wasm vulnerability into DOM-Based XSS or Server-Side Remote Code Execution (RCE).

## References

- [W3C WebAssembly Core Specification](https://webassembly.github.io/spec/core/)
- [WebAssembly System Interface (WASI)](https://wasi.dev/)
- [MDN Web Docs: WebAssembly Concepts](https://developer.mozilla.org/en-US/docs/WebAssembly/Concepts)
