# WebAssembly Resource Exhaustion and Concurrency

|ID          |
|------------|
|WSTG-WASM-06|

## Summary

WebAssembly (Wasm) executes at near-native speed inside browsers, Node.js, and server-side or edge WebAssembly System Interface (WASI) runtimes. While the Wasm sandbox restricts unauthorized host access, it does not automatically enforce Central Processing Unit (CPU) time quotas, compilation budgets, or strict memory ceilings unless the host explicitly configures them. Furthermore, multi-threaded Wasm workloads built with the WebAssembly threads proposal share a single linear memory buffer (`SharedArrayBuffer`) across workers, introducing concurrency hazards that do not exist in single-threaded modules.

Weak resource governance and unsafe concurrency patterns in Wasm deployments can lead to:

- Denial of Service (DoS) by freezing the browser main thread or exhausting server-side worker pools through unbounded loops or recursive execution.
- Out-of-Memory (OOM) crashes and noisy-neighbor degradation when modules allocate excessive linear memory via `memory.grow` without host-enforced page ceilings.
- Excessive CPU and memory consumption during Just-In-Time (JIT) or Ahead-Of-Time (AOT) compilation when applications accept untrusted `.wasm` modules or plugins.
- Time-of-Check to Time-of-Use (TOCTOU) race conditions, data corruption, and thread deadlocks when multiple threads read, mutate, or wait on shared linear memory without proper synchronization.
- Overly permissive cross-origin resource exposure when applications enable Cross-Origin Opener Policy (COOP) and Cross-Origin Embedder Policy (COEP) headers to unlock `SharedArrayBuffer`.

This test case provides a methodology for testing resource limits, compilation resilience, shared-memory concurrency, and cross-origin isolation configurations.

## Test Objectives

- Verify whether linear memory and table growth (`memory.grow`, `table.grow`) are bounded by explicit maximum limits and host resource caps.
- Test whether long-running loops or algorithmic complexity in Wasm exports can starve browser threads or server-side runtimes lacking fuel metering or epoch interruption.
- Assess platforms that compile user-supplied Wasm modules for compilation-time and memory-usage exhaustion (compilation bombs).
- Identify TOCTOU race conditions, unsynchronized shared-state mutations, and unbounded wait deadlocks in multi-threaded modules using `SharedArrayBuffer`.
- Audit `COOP`, `COEP`, and Cross-Origin Resource Policy (CORP) headers deployed to enable Wasm threads for unintended cross-origin exposure.

## How to Test

Note: This test case builds on the section enumeration and runtime hooking techniques covered in [WebAssembly Static Analysis](02-WebAssembly_Static_Analysis.md) and [WebAssembly Dynamic Analysis](03-WebAssembly_Dynamic_Analysis.md).

### Testing for Unbounded Memory and Table Growth

Each WebAssembly linear memory page is 64 KiB. Non-shared memories may omit a declared maximum page count, allowing a module to call `memory.grow` until the host runtime exhausts available memory (up to 4 GiB for standard 32-bit memories, or higher for `memory64`). Similarly, `table.grow` can expand function or reference tables if left unbounded.

1. Inspect the module's `Memory`, `Table`, and `Import` sections using the WebAssembly Binary Toolkit (WABT) to check whether maximum limits are declared:

   ```sh
   wasm-objdump -x -j Memory module.wasm
   wasm-objdump -x -j Table module.wasm
   wasm-objdump -x -j Import module.wasm
   ```

   Look for entries without a `max=` parameter (for example, `memory[0] pages: initial=2` instead of `initial=2 max=256`). Note that shared memories are required by the specification to declare a `max` value, but that ceiling may still be set excessively high.

2. Check the disassembly for `memory.grow` or `table.grow` instructions reachable from user-controlled inputs:

   ```sh
   wasm2wat module.wasm | grep -E "memory\.grow|table\.grow"
   ```

3. In browser or server-side endpoints that pass user-controlled sizes, counts, or large payloads into Wasm exports (such as image decoders, archive extractors, or JSON parsers), submit incrementally larger allocation requests and monitor memory consumption:
   - In browsers, monitor tab heap and Wasm memory growth in DevTools (**Memory** tab) and check whether the tab crashes with an OOM error.
   - In server-side or edge runtimes, test whether a single request can trigger an OOM kill of the worker process or degrade concurrent requests from other users.

### Testing for CPU Exhaustion and Missing Execution Limits

WebAssembly bytecode does not include built-in preemption. Without host-enforced execution limits, a module executing an infinite loop, heavy cryptographic iteration, or catastrophic regular-expression backtracking blocks its execution thread indefinitely.

1. Identify exported functions whose iteration counts, recursion bounds, or loop termination conditions depend on user input.
2. Test browser-side execution placement:
   - Determine whether heavy Wasm functions run on the browser's main user interface (UI) thread or inside a dedicated Web Worker.
   - Supply worst-case inputs and verify whether the page becomes unresponsive, blocking user interaction and network callbacks.
3. Test server-side and edge runtimes for execution quotas:
   - On platforms running untrusted plugins or user-driven Wasm workloads (such as Wasmtime, Wasmer, or edge workers), send inputs designed to trigger high iteration counts or long-running loops.
   - Verify whether the runtime cleanly aborts execution after a bounded timeout or instruction budget (for example, via Wasmtime's fuel metering or epoch-based interruption) and returns a controlled error rather than hanging the worker thread or exhausting the thread pool.

### Testing for Compilation Bombs in Untrusted Module Loaders

Applications that allow users or tenants to upload custom Wasm plugins, filters, or smart-contract-style extensions must parse and compile untrusted binaries. Maliciously crafted modules can trigger superlinear compile times or memory spikes in optimizing JIT/AOT compilers even before a single instruction executes.

When testing platforms that accept untrusted `.wasm` uploads:

1. Check whether the host enforces strict file-size limits and structural validation before invoking `WebAssembly.compile` or server-side AOT compilation.
2. Test resilience against structural stress cases in a controlled staging environment:
   - Deeply nested control-flow blocks (`block` / `loop` / `if`) or massive `br_table` jump tables.
   - Single functions containing tens of thousands of local variables or arithmetic instructions designed to stress register allocation in optimizing compilers (such as Cranelift or V8 TurboFan).
   - Modules with large numbers of types, functions, or passive data segments.
3. Measure compilation latency and peak host memory usage. Confirm that compilation is isolated with strict timeouts and memory limits rather than blocking the main application server.

### Testing for Shared Memory Race Conditions and TOCTOU

Modules compiled with POSIX threads (for example, Emscripten `-pthread` or Rust `atomics` + `bulk-memory`) share a single `WebAssembly.Memory({ shared: true })` backed by a `SharedArrayBuffer` across the main thread and Web Workers.

When the host or one thread validates data stored in shared linear memory before another thread (or the Wasm module) consumes it, an attacker who can trigger concurrent operations can modify the shared bytes between the check and the use (double-fetch / TOCTOU).

Consider a pattern where JavaScript validates a command header inside shared memory before signaling a Wasm worker to execute it:

```javascript
// Main thread writes and validates a request in SharedArrayBuffer
const sharedView = new Uint8Array(sharedMemory.buffer);
if (isAllowedCommand(sharedView, offset)) {
  // Race window: another worker sharing the same buffer can overwrite
  // bytes at `offset` before the Wasm worker reads and executes them.
  worker.postMessage({ action: "run", offset });
}
```

To test for shared-memory concurrency flaws:

1. Confirm whether the module uses shared memory and atomic instructions:

   ```sh
   wasm-objdump -x -j Memory module.wasm | grep shared
   wasm-objdump -x -j Import module.wasm | grep shared
   wasm2wat module.wasm | grep -E "atomic\."
   ```

2. Identify shared buffers, ring buffers, or state structs in `SharedArrayBuffer` that are accessed from both JavaScript and Wasm workers.
3. Look for non-atomic loads/stores (`i32.load`, `i32.store`) operating on shared flags, lengths, or indices instead of atomic operations (`i32.atomic.load`, `i32.atomic.rmw.cmpxchg`).
4. Test for TOCTOU by spawning concurrent requests or modifying the target offset in `SharedArrayBuffer` in a tight loop from the browser console or a worker while triggering the validation-and-execution flow. Merely observing that a worker reads a mutated value is not sufficient, as the worker may legitimately read updated shared state. Confirm that validation and consumption operate on the same logical request and that the mutation produces a security-relevant bypass of the validation—for example, passing an authorization, bounds, or command-allowlist check with a benign value, overwriting that same shared offset with a disallowed value before consumption, and verifying that the Wasm worker executes the unvalidated request rather than rejecting it or operating on a private copy.
5. Check for unbounded blocking waits (`memory.atomic.wait32`, `memory.atomic.wait64`, or `Atomics.wait` with no timeout) inside worker threads, and separately check for main-thread misuse—calling `Atomics.wait` on the browser's main thread throws a `TypeError` (and blocking `memory.atomic.wait*` traps) rather than blocking, so main-thread code must use `Atomics.waitAsync`. In workers, trigger error paths or dropped messages between threads to verify whether a missing `memory.atomic.notify` or an unreleased mutex permanently deadlocks worker threads and starves the worker pool.

### Auditing Cross-Origin Isolation (`COOP`/`COEP`) and Side-Channel Exposure

Browsers restrict `SharedArrayBuffer` to cross-origin isolated contexts to mitigate speculative execution side-channel attacks (such as Spectre). To enable Wasm threads, applications must serve:

- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp` (or `credentialless`)

Because `COEP: require-corp` blocks cross-origin subresources unless they opt in, developers sometimes misconfigure `Cross-Origin-Resource-Policy` (CORP) or Cross-Origin Resource Sharing (CORS) headers across their application to make assets load.

1. Inspect HTTP response headers for the page hosting the threaded Wasm module and its subresources:
   - Verify whether `window.crossOriginIsolated` evaluates to `true` in the browser console.
   - Check whether sensitive user-specific subresources (such as private media, images, or personalized scripts) were hastily configured with `Cross-Origin-Resource-Policy: cross-origin`. While permissive CORP does not allow cross-origin JavaScript to read the raw response body, it permits third-party origins to embed the resource—potentially enabling metadata leaks, Cross-Site Script Inclusion (XSSI), or side-channel exposure in a cross-origin isolated attacker page.
   - Separately verify that authenticated endpoints (such as JSON APIs) were not configured with overly broad CORS headers (for example, reflected `Access-Control-Allow-Origin` values alongside `Access-Control-Allow-Credentials: true`), which would allow cross-origin JavaScript to directly read sensitive response data.
2. Check whether the application runs untrusted Wasm code or third-party scripts inside the same cross-origin isolated origin as sensitive secrets:
   - In a cross-origin isolated context, browsers expose higher-resolution timers (`performance.now()`) and `SharedArrayBuffer`-based counting threads, which can facilitate microarchitectural timing attacks against sensitive data residing in the same renderer process.

### Analysis Notes and Limitations

- Shared memory maximum requirement: Unlike non-shared `WebAssembly.Memory`, the WebAssembly threads specification requires every shared memory to declare a `maximum` page count. However, a very large declared maximum (for example, `65536` pages / 4 GiB) still permits excessive memory reservation or growth if the host does not enforce a lower cap.
- Browser versus server-side impact: In a browser, CPU or memory exhaustion primarily impacts the local user's tab (unless triggered persistently via stored input for other visitors). On multi-tenant server-side and edge Wasm platforms, missing execution or memory limits represent a high-severity availability risk affecting all tenants sharing the host.
- Deterministic versus probabilistic testing: TOCTOU race conditions on `SharedArrayBuffer` are timing-sensitive and may require repeated concurrent runs or artificial latency (such as DevTools CPU throttling) to reproduce reliably.

## Related Test Cases

- [WebAssembly Static Analysis](02-WebAssembly_Static_Analysis.md)
- [WebAssembly Dynamic Analysis](03-WebAssembly_Dynamic_Analysis.md)

## Remediation

- Always define conservative `maximum` page and table limits in `WebAssembly.Memory` and `WebAssembly.Table` descriptors, and enforce host-level memory caps (such as `StoreLimits` in Wasmtime) for server-side workloads.
- Offload long-running browser Wasm workloads to dedicated Web Workers so they cannot freeze the main UI thread, and enforce timeouts via `Worker.terminate()`.
- On server-side and edge runtimes, enforce strict execution budgets using fuel metering or epoch-based interruption so runaway loops terminate deterministically.
- When compiling untrusted Wasm modules, enforce strict binary size and complexity limits, use streaming or baseline compilation modes where appropriate, and isolate compilation in resource-bounded worker processes with timeouts.
- Copy validated input data out of `SharedArrayBuffer` into private, non-shared memory (or pass immutable copies) before acting on it to eliminate TOCTOU windows. Use atomic operations (`i32.atomic.*` / `Atomics`) for shared synchronization primitives, and apply an appropriate synchronization protocol (such as a lock or sequence counter) where compound operations or multi-field state updates require consistency across multiple values, since atomic operations alone do not make multi-step or cross-field updates safe. Enforce bounded timeouts on worker-side `memory.atomic.wait` and `Atomics.wait` calls (using `Atomics.waitAsync` on the main thread) so faulted threads cannot deadlock the worker pool or throw runtime errors.
- Apply `Cross-Origin-Resource-Policy: cross-origin` only to genuinely public static assets (rather than blanket-applying it or loosening CORS on authenticated endpoints) when enabling `COOP`/`COEP`, and never execute untrusted Wasm workloads in the same origin or process as sensitive authenticated data.

## Tools

- [WebAssembly Binary Toolkit (WABT)](https://github.com/WebAssembly/wabt) - `wasm-objdump` and `wasm2wat` for inspecting declared memory/table limits, `shared` flags, `memory.grow`, and atomic instructions.
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/wasm/) and [Firefox DevTools](https://firefox-source-docs.mozilla.org/devtools-user/) - Monitoring memory growth, CPU throttling to widen race windows, and inspecting `COOP`/`COEP`/`CORP` response headers.
- [Wasmtime](https://github.com/bytecodealliance/wasmtime) - Supports `--fuel`, `--epoch-interruption`, and `StoreLimits` for testing and verifying resource-bounded Wasm execution.

## References

- [MDN Web Docs: `SharedArrayBuffer` and Cross-Origin Isolation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)
- [MDN Web Docs: Cross-Origin-Opener-Policy (COOP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy)
- [MDN Web Docs: Cross-Origin-Embedder-Policy (COEP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)
- [WebAssembly Threads Proposal](https://github.com/WebAssembly/threads/blob/main/proposals/threads/Overview.md)
- [Wasmtime Documentation: Security and Resource Limits](https://docs.wasmtime.dev/security.html)
