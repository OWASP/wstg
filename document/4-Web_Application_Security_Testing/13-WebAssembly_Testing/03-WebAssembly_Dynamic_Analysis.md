# WebAssembly Dynamic Analysis

|ID          |
|------------|
|WSTG-WASM-03|

## Summary

Dynamic analysis evaluates a WebAssembly (Wasm) module by executing it within its host runtime (primarily modern web browsers) and observing its behavior in real time. While static analysis maps declared interfaces and embedded data at rest, dynamic analysis examines runtime execution state, live linear memory mutations, cross-boundary data flows between JavaScript and Wasm, and client-side decision logic.

Because browser-based WebAssembly runs inside an isolated sandbox without direct access to the DOM, network, or platform APIs, it interacts with the application exclusively through imported host functions and exported module entry points. Furthermore, WebAssembly only handles primitive numeric types (`i32`, `i64`, `f32`, `f64`). Higher-level data types - such as strings, arrays, JSON payloads, and cryptographic tokens - are passed across the boundary as numeric memory pointers (offsets) into the module's linear memory.

This test case provides an operational methodology for:

- Intercepting the module lifecycle using zero-code fetch breakpoints and automated ES6 boundary proxies.
- Resolving memory pointers passed to exported functions and extracting plaintext data directly from linear memory.
- Inspecting and altering live linear memory via native browser developer tools.
- Setting runtime instruction breakpoints on decompiled WebAssembly Text (WAT) representations.
- Interacting directly with exported functions from the browser console.

## Test Objectives

- Intercept the module loading pipeline (`WebAssembly.instantiate` and `WebAssembly.instantiateStreaming`) to capture references to active instances and memory segments.
- Capture and log bidirectional function calls, arguments, memory pointers, and return values crossing the JS/Wasm boundary without violating runtime proxy invariants.
- Dereference numeric memory pointers to reconstruct strings, structures, and sensitive parameters exchanged between JavaScript and WebAssembly.
- Search, inspect, and monitor live linear memory (`WebAssembly.Memory`) for transient secrets, unencrypted credentials, and authorization states using native browser tooling.
- Debug executing modules at runtime using instruction-level breakpoints within disassembled WAT views.
- Test client-side business logic and validation routines by invoking exported functions with crafted inputs via the browser console.

## How to Test

### Manual Interception via DevTools Fetch Breakpoints

For rapid, zero-extension analysis, testers can freeze execution prior to module instantiation using native browser breakpoints:

1. Open DevTools (`F12`) and select the **Sources** tab.
2. In the right-hand panel, expand **XHR/fetch Breakpoints** and click **+**.
3. Enter `.wasm` (so the breakpoint triggers when the request URL contains `.wasm`).
4. Refresh the page.
5. Execution pauses as soon as the network request for the `.wasm` binary is initiated. At this stage, testers have two options:
   - **Manual Scope Inspection:** Use **Step Over** (`F10`) or **Step Out** (`Shift+F11`) to trace the promise resolution up to the `WebAssembly.instantiate` call and inspect the `importObject` in the **Scope** pane.
   - **Console Hook Injection:** Paste the boundary proxy script (detailed in the next section) directly into the **Console** and press **Resume script execution** (`F8`) to hook the module dynamically without external tools.

### Automated Boundary Interception via ES6 Proxies

WebAssembly exports are non-configurable and non-writable data properties on the module instance. Directly wrapping `instance.exports` in a standard proxy target causes modern JavaScript engines (such as V8) to throw a `TypeError` regarding proxy invariants.

To capture both imports and exports transparently without breaking host runtime initialization (e.g., Emscripten stack setup), wrap targets by cloning descriptors into a plain mutable object proxy.

While execution is paused at the `.wasm` fetch breakpoint, paste the following script into the **Console** and press `F8` to resume execution (alternatively, inject it prior to page load via an intercepting proxy):

```javascript
(() => {
  // Clone descriptors into a plain object to satisfy ECMAScript proxy invariants
  const createSafeProxy = (realObj, boundaryName) => {
    const mutableTarget = Object.assign({}, realObj);
    return new Proxy(mutableTarget, {
      get(target, prop) {
        const val = realObj[prop];
        if (typeof val !== "function") return val;
        return function (...args) {
          console.group(`[Wasm Boundary] ${boundaryName} -> ${String(prop)}()`);
          console.log("Arguments:", args);
          try {
            const res = val.apply(this, args);
            console.log("Returned:", res);
            return res;
          } catch (err) {
            console.error("Execution Error:", err);
            throw err;
          } finally {
            console.groupEnd();
          }
        };
      }
    });
  };

  const hookImports = (importObject = {}) =>
    Object.fromEntries(
      Object.entries(importObject).map(([k, v]) => [
        k,
        typeof v === "object" && v !== null ? createSafeProxy(v, `Import [${k}]`) : v
      ])
    );

  const hookInstance = (instance, importObject) => {
    window._wasmInstance = instance;
    window._wasmMemory = instance.exports.memory || importObject?.env?.memory;
    const safeExports = createSafeProxy(instance.exports, "Export");
    console.log("[+] Live Wasm module hooked (Imports & Exports captured).");
    return new Proxy(instance, {
      get: (t, p) => (p === "exports" ? safeExports : Reflect.get(t, p, t))
    });
  };

  const origStreaming = WebAssembly.instantiateStreaming;
  WebAssembly.instantiateStreaming = async (source, imports = {}) => {
    const res = await origStreaming(source, hookImports(imports));
    return { module: res.module, instance: hookInstance(res.instance, imports) };
  };

  const origInstantiate = WebAssembly.instantiate;
  WebAssembly.instantiate = async (bytesOrModule, imports = {}) => {
    const res = await origInstantiate(bytesOrModule, hookImports(imports));
    return res.instance
      ? { module: res.module, instance: hookInstance(res.instance, imports) }
      : hookInstance(res, imports);
  };
})();
```

### Resolving Pointers and Reading Memory

When interacting with web forms or APIs, WebAssembly functions accept pointers rather than raw strings. For example, passing the string `"hello"` to an Emscripten-compiled export produces console output similar to:

```text
[Wasm Boundary] Export -> _emscripten_stack_alloc()
Arguments: [6]
Returned: 65520

[Wasm Boundary] Export -> greetings()
Arguments: [65520]
Returned: undefined
```

In this trace:

1. `_emscripten_stack_alloc(6)` allocates 6 bytes (5 ASCII characters + null terminator `\0`) and returns memory pointer `65520`.
2. `greetings(65520)` takes the pointer as its argument.

Testers can dereference this pointer and read the underlying value directly from linear memory via the browser console:

```javascript
// Read null-terminated string at a specific pointer offset
function readWasmString(offset, maxLength = 256) {
  if (!window._wasmMemory) return null;
  const memoryView = new Uint8Array(window._wasmMemory.buffer);
  let end = offset;
  while (end < offset + maxLength && memoryView[end] !== 0) {
    end++;
  }
  return new TextDecoder("utf-8").decode(memoryView.slice(offset, end));
}

// Example: Dereference the captured pointer 65520
console.log("Extracted String:", readWasmString(65520));
// Output: "hello"
```

### Live Memory Inspection via DevTools Memory Inspector

Linear memory is exposed as an `ArrayBuffer`. When cryptographic routines, session tokens, or API credentials are decrypted or constructed during runtime, they are held in this buffer.

Modern Chromium-based browsers feature a built-in **Memory Inspector**:

1. Open DevTools -> **Console**.
2. Type `window._wasmMemory.buffer` and press Enter.
3. Click the small memory icon next to the returned `ArrayBuffer` (or right-click and select **Inspect in Memory Inspector**).
4. The Memory Inspector panel provides an interactive hex/ASCII viewer:
   - Enter an offset (such as `65520` or hex `0x10000`) in the navigation bar to jump directly to target data.
   - Inspect data representations as unsigned/signed 8/16/32-bit integers, floating-point numbers, or ASCII characters.

#### Searching Live Memory for Transient Indicators

To scan the entire active linear memory for secrets that were not visible during static analysis:

```javascript
function searchLiveMemory(pattern) {
  if (!window._wasmMemory) {
    console.error("No active Wasm memory reference captured.");
    return [];
  }
  const buffer = new Uint8Array(window._wasmMemory.buffer);
  const text = new TextDecoder("utf-8", { fatal: false }).decode(buffer);
  const regex = new RegExp(pattern, "gi");
  const matches = [];
  let match;
  while ((match = regex.exec(text)) !== null) {
    matches.push({ match: match[0], offset: match.index });
  }
  return matches;
}

// Example: Search live memory for JWTs, bearer tokens, or API keys
console.table(searchLiveMemory("(Bearer\\s[A-Za-z0-9\\-_\\.]+|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9-_\\.]+)"));
```

### Interactive Invocation and Argument Crafting

Testers can validate server-side enforcement by invoking exported functions directly from the Developer Console, bypassing client-side UI limitations.

When invoking an export that requires a complex parameter (like a string), allocate or write the payload into memory first:

```javascript
function writeStringToMemory(str) {
  const encoded = new TextEncoder().encode(str);
  const alloc = window._wasmInstance.exports.malloc || window._wasmInstance.exports._emscripten_stack_alloc;
  let ptr;

  if (typeof alloc === "function") {
    ptr = alloc(encoded.length + 1);
  } else {
    // Fallback: Use scratchpad offset for local validation
    ptr = 1024;
  }

  const memory = new Uint8Array(window._wasmMemory.buffer);
  memory.set(encoded, ptr);
  memory[ptr + encoded.length] = 0; // Null terminator

  return { ptr, len: encoded.length };
}

// Example: Directly call validation logic with custom payload
const tokenPayload = writeStringToMemory("admin_test_token");
const isAuthorized = window._wasmInstance.exports.verify_token(tokenPayload.ptr, tokenPayload.len);
console.log("Validation output:", isAuthorized);
```

### Bytecode Execution Debugging

If debug symbols (DWARF) are stripped, modern browsers automatically disassemble the binary into the WebAssembly Text Format (WAT) for debugging:

1. In DevTools, open the **Sources** tab.
2. Locate the loaded module under the `wasm://` scheme or host domain tree.
3. Review the disassembled instruction listing (`call`, `i32.load`, `local.get`, `br_if`).
4. Click on a line number to set a breakpoint at critical branching or validation points.
5. Trigger the application flow:
   - When execution halts, inspect the **Scope** window to observe the values of stack registers and local variables.
   - Use **Step Over** (`F10`) and **Step Into** (`F11`) to trace conditional execution branches.

*Note on DWARF Metadata:* If the target module retains DWARF symbols, install the **C/C++ WebAssembly Debugging** browser extension to debug against the original C/C++ or Rust source files rather than disassembled WAT.

## Analysis Notes and Limitations

- **Proxy Invariant Rules:** Directly proxying `instance.exports` violates ECMAScript proxy invariants for non-configurable properties. Always clone descriptors into a mutable target object (`Object.assign({}, realObj)`) when building wrappers around WebAssembly exports.
- **Memory Detachment:** Calling `memory.grow` reallocates linear memory, detaching existing `ArrayBuffer` instances. Cached typed arrays (`Uint8Array`) will become zero-length, requiring scripts to re-acquire `window._wasmMemory.buffer`.
- **String Encodings and Representations:** Strings in WebAssembly are not universally null-terminated. While C/C++ modules (e.g., compiled via Emscripten) typically rely on null-terminated C-strings, modules compiled with Go represent strings as pointer-plus-length slices without a trailing null byte. Attempting to read until a null terminator in Go binaries can cause buffer over-reads or corrupted data; always verify the module's target ABI and calling conventions before dereferencing linear memory.
- **Out-of-Bounds Traps:** Passing arbitrary integer values to functions expecting valid memory pointers will trigger a WebAssembly execution trap (`RuntimeError: memory access out of bounds`), immediately halting execution.

## Tools

- **Chrome / Firefox DevTools** - Native WebAssembly debugging, instruction stepping, and the Chrome DevTools Memory Inspector.
- **C/C++ WebAssembly Debugging (Browser Extension)** - Official browser extension enabling DWARF-based source-level debugging inside DevTools.
- **Playwright / Puppeteer** - Automation frameworks providing direct access to the Chrome DevTools Protocol (`Debugger` and `Runtime` domains) for scriptable testing.
- **Burp Suite / ZAP** - Intercepting HTTP proxies used to inject boundary-logging scripts into HTML responses prior to module execution.

## References

- [Chrome DevTools: Debugging WebAssembly with modern tools](https://developer.chrome.com/docs/devtools/wasm/)
- [Chrome DevTools: Inspecting ArrayBuffers with the Memory Inspector](https://developer.chrome.com/docs/devtools/memory-inspector/)
- [WebAssembly JavaScript Interface (W3C Specification)](https://www.w3.org/TR/wasm-js-api-1/)
- [MDN Web Docs: Working with WebAssembly Memory](https://developer.mozilla.org/en-US/docs/WebAssembly/JavaScript_interface/Memory)
- [ManuMassi/vuln_wasm](https://github.com/ManuMassi/vuln_wasm) - Collection of vulnerable WebAssembly applications (client-side and server-side) built for the study of WebAssembly security.
