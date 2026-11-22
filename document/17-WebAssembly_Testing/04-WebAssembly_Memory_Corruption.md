# WebAssembly Memory Corruption

|ID          |
|------------|
|WSTG-WASM-04|

## Summary

WebAssembly (Wasm) isolates executable bytecode and the hardware call stack from the module's addressable linear memory (`WebAssembly.Memory`). While this prevents attackers from injecting executable shellcode or overwriting hardware return addresses, modules compiled from memory-unsafe languages (such as C and C++) manage their own internal memory layout (including an unmanaged shadow stack and dynamic heap) within a flat, contiguous byte array.

Standard operating system mitigations, such as Address Space Layout Randomization (ASLR), per-function stack canaries, and read-only page permissions (`.rodata` protection), are absent within standard WebAssembly linear memory. Every allocated page within `WebAssembly.Memory` is readable and writable by default, and runtime bounds checks only trigger a trap (`RuntimeError: memory access out of bounds`) when an access exceeds the outer boundary of all allocated 64 KiB pages.

Consequently, spatial and temporal memory safety vulnerabilities allow attackers to silently corrupt adjacent data structures inside linear memory without crashing the module. Depending on the application architecture, linear memory corruption can lead to:

- Bypassing authentication or business logic by overwriting adjacent stack variables or heap chunks.
- Escalating buffer overflows into Cross-Site Scripting (XSS) or Remote Code Execution (RCE) by corrupting strings passed to JavaScript (JS) sinks or inline execution macros.
- Hijacking internal module control flow by corrupting function table indices consumed by `call_indirect` instructions.
- Reading or writing arbitrary linear memory locations via format string vulnerabilities or integer truncation across the JS/Wasm boundary.
- Corrupting writable global state (`.data` and `.bss`) by overflowing the unmanaged shadow stack through attacker-controlled recursion depth or oversized stack frames without trapping.

## Test Objectives

- Exploit stack buffer overflows to overwrite adjacent variables, authorization flags, or command buffers in linear memory.
- Trigger shadow-stack exhaustion via deep recursion or oversized stack frames to overwrite global (`.data` and `.bss`) state.
- Corrupt static `.data` segments or stack buffers passed to JavaScript sinks and inline macros (such as `EM_ASM`) to achieve XSS or host code execution.
- Subvert internal module control flow by overwriting function pointers (`__indirect_function_table` indices) used in `call_indirect` dispatches.
- Exploit heap Use-After-Free (UAF) and double-free conditions to overwrite the contents of freed-and-reallocated chunks and subvert authentication or state checks.
- Trigger format string vulnerabilities and 32-bit integer truncations across the JS/Wasm boundary to bypass host validation and achieve arbitrary memory reads or writes.

## How to Test

Note: This test case assumes familiarity with the static inspection and runtime memory hooking techniques covered in [WebAssembly Static Analysis (WSTG-WASM-02)](02-WebAssembly_Static_Analysis.md) and [WebAssembly Dynamic Analysis (WSTG-WASM-03)](03-WebAssembly_Dynamic_Analysis.md).

### Testing for Stack Buffer Overflows and Host Sink Escalation

When local arrays and variables have their addresses taken in C/C++, compilers allocate them contiguously on the unmanaged shadow stack inside linear memory. An unbounded write (e.g., via `strcpy`, `sprintf`, or `strncpy` where the length parameter is derived from `strlen(source)` rather than the destination capacity) overflows into adjacent variables on the shadow stack or corrupts writable `.data` segments.

Memory corruption inside the Wasm sandbox escalates into a critical host vulnerability when corrupted memory is passed back to JavaScript glue code, such as Document Object Model (DOM) sinks, or evaluated via toolchain macros such as Emscripten's `EM_ASM`.

Consider a vulnerable C function compiled with Emscripten:

```c
void render_greeting(char* username) {
    char script_tpl[64] = "console.log('Session initialized')";
    char display_name[24];

    // Flaw: length is derived from untrusted input rather than destination size (24)
    strncpy(display_name, username, strlen(username));

    EM_ASM({
        eval(UTF8ToString($0));
        console.log("User: " + UTF8ToString($1));
    }, script_tpl, display_name);
}
```

To test and exploit this condition:

1. Identify functions that copy user-controlled input into local buffers adjacent to state variables, static `.data` templates, or buffers passed to host imports (`EM_ASM`, `emscripten_run_script`, or DOM manipulation wrappers).
2. Determine the exact byte distance (delta) between the start of the input buffer (`display_name`) and the target buffer (`script_tpl`) on the shadow stack (e.g., `32` bytes due to stack alignment).
3. Supply a payload that pads the input buffer and overwrites the adjacent command or template buffer with an execution payload:
   - Browser host (DOM XSS):

    ```text
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAalert(document.domain);//
    ```

   - Server-side or Node.js host (RCE):

    ```text
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAconst { execSync } = require('child_process'); console.log(execSync('id').toString());//
    ```

4. Trigger the function and verify whether the overwritten memory buffer executes within the host JavaScript context.

### Testing for Shadow-Stack Exhaustion via Deep Recursion

In raw `wasm-ld` invocations and legacy or custom toolchain builds compiled without `--stack-first`, the shadow stack is placed after the writable `.data` and `.bss` sections and grows downward toward them. Unbounded recursion or large dynamic stack frames (`alloca`, oversized local arrays) in such builds do not crash the module: once the stack pointer descends past the bottom of the stack region, each new frame silently overwrites globals and static data.

Consider a module that derives recursion depth from user input:

```c
int is_admin = 0; // Zero-initialized global stored in .bss, below the shadow stack

void process(int depth, char* note) {
    char frame[64];
    strncpy(frame, note, 64); // Attacker-controlled frame contents
    if (depth > 0)
        process(depth - 1, note);
}

void handle_request(int depth, char* note) {
    // Flaw: the depth bound exceeds the shadow stack capacity (64 KiB)
    if (depth < 1500)
        process(depth, note);
}
```

To test for shadow-stack exhaustion:

1. Check whether the module places the shadow stack above `.data` and `.bss` (by inspecting the initial value of the stack pointer `global[0]` relative to data segment offsets) and estimate the per-frame cost (here, roughly 80 bytes: a 64-byte buffer plus saved arguments and alignment).
2. Drive the recursion depth or allocation size from user input until the cumulative frame size crosses the bottom of the stack region (e.g., submit `depth` values in increasing steps).
3. Verify whether the global (`is_admin`) now holds attacker-influenced frame contents instead of the module trapping (a clean crash indicates the depth bound remained within the stack region or hit address `0`, not that the recursion flaw is absent).
4. Confirm that the corruption is silent in uninstrumented builds: builds compiled with `-sSTACK_OVERFLOW_CHECK` or `-sASSERTIONS` abort with `Stack overflow!` when Emscripten's stack cookies are clobbered, whereas uninstrumented builds without `--stack-first` corrupt `.data` and `.bss` without any error.
5. Contrast against a `--stack-first` build, where downward overflow immediately passes below address `0` and traps with `RuntimeError: memory access out of bounds`.

### Testing for Control-Flow Hijacking via Indirect Calls (`call_indirect`)

Although attackers cannot overwrite return addresses on the managed call stack, C/C++ function pointers and C++ virtual method tables (`vtables`) are stored in linear memory as 32-bit integers representing indices into the module's `__indirect_function_table`. At runtime, these indices are invoked via the `call_indirect` instruction.

Consider a function where a buffer sits adjacent to a function pointer on the shadow stack:

```c
bool run_privileged_task() { return true; }  // Table index 1
bool run_standard_task()   { return false; } // Table index 2

bool dispatch_task(char* token) {
    bool (*task_handler)(void) = 0;
    char token_buf[16];

    strcpy(token_buf, token); // Overflows into task_handler

    if (task_handler == 0) {
        if (strcmp(token_buf, "valid_token") == 0)
            task_handler = &run_privileged_task;
        else
            task_handler = &run_standard_task;
    }
    return task_handler(); // Dispatched via call_indirect
}
```

To test for indirect call redirection:

1. Inspect the module's `Elem` section to map the valid function indices registered in `__indirect_function_table` (for example, index `1` for `run_privileged_task` and index `2` for `run_standard_task`).
2. Verify that the target function shares the exact Wasm type signature `(param ...) (result ...)` expected by the `call_indirect` instruction; otherwise, the runtime will trap with a signature mismatch.
3. Overflow the adjacent buffer (`token_buf[16]`) to overwrite the stored `i32` function pointer with the target table index (`0x01`). Because `task_handler` is initialized to `0` and linear memory is little-endian, writing `\x01` (plus the trailing null byte from `strcpy`) sets the index to `1`; adjust the padding length if compiler stack alignment inserts extra bytes between the buffer and the pointer:

   ```javascript
   // Padding to reach task_handler (adjust if stack alignment adds bytes), followed by table index 1
   const payload = "A".repeat(16) + "\x01";
   ```

4. Submit the payload and observe whether `call_indirect` redirects execution to the privileged function (`run_privileged_task`) without supplying a valid token.

### Testing for Heap Use-After-Free (UAF) and Double Free

WebAssembly modules compiled from C/C++ bundle a linear-memory allocator (such as `dlmalloc` or `emmalloc`) to manage dynamic heap chunks. Because WebAssembly lacks randomized heap allocation (no ASLR), heap behavior is strictly deterministic: when a chunk is freed via `free()`, it is placed into a freelist bin and immediately reused for subsequent `malloc()` requests of a matching size.

If the application retains a dangling pointer to a freed struct on the heap, an attacker who can trigger a new allocation of the same size can overwrite the freed struct's fields.

```c
typedef struct {
    char username[32];
    char role[8];
} UserSession;

UserSession *active_session;

void create_session(const char* name) {
    active_session = malloc(sizeof(UserSession)); // Allocates 40-byte chunk
    strncpy(active_session->username, name, sizeof(active_session->username) - 1);
    strncpy(active_session->role, "guest", sizeof(active_session->role));
}

void close_session() {
    free(active_session); // Flaw: pointer is not cleared (dangling pointer)
}

void store_note(int size, char* note) {
    char* buf = malloc(size);
    strcpy(buf, note);
}
```

To test for deterministic Heap UAF:

1. Identify workflows where an object or structure is freed (`close_session`), but references to the pointer remain accessible to validation routines (e.g., an authorization check reading `active_session->role`).
2. Trigger the deallocation function to place the target chunk into the allocator's freelist.
3. Trigger a user-controlled allocation (`store_note`) requesting a byte size equal or close to the freed structure (`40` bytes). The deterministic allocator will assign the exact same linear memory address to the new buffer.
4. Populate the new allocation with padding aligned to the target struct's layout (`32` bytes of `'A'` followed by `"admin"`).
5. Invoke the validation routine that dereferences the dangling pointer (`active_session->role`) and confirm whether it reads the attacker-supplied value (`"admin"`).

A closely related condition is the double free (`free()` invoked twice on the same chunk). Bundled linear-memory allocators perform limited metadata validation compared to hardened native allocators, and layout is fully deterministic. To test:

1. Invoke the deallocation routine twice on the same object and observe whether the allocator aborts (`dlmalloc` ships basic consistency checks) or silently corrupts the freelist (`emmalloc` performs minimal validation).
2. Perform subsequent allocations in the relevant size classes and check whether two logically distinct objects resolve to the same linear memory address (overlapping chunks), allowing a write through one handle to corrupt the other.

### Testing for Format String Vulnerabilities in Linear Memory

When C/C++ functions pass user-controlled strings directly as the format argument to `printf`, `sprintf`, or `snprintf` (e.g., `printf(user_input)`), the WebAssembly module is vulnerable to format string attacks.

In WebAssembly's calling convention, fixed function arguments are passed in virtual local variables, which cannot be read by `printf`. However, variadic arguments (`...`) and local buffers are placed directly on the unmanaged shadow stack in linear memory. Consequently, format specifiers walk up the shadow stack inside linear memory. (Emscripten's musl-based `libc` supports `%n` unconditionally and single-digit positional parameters such as `%2$n`, so classic format-string primitives carry over to default builds.)

1. Arbitrary stack and memory read (`%p`, `%x`, `%s`): Supplying chained format specifiers such as `%p|%p|%p|%p` or `%s` reads values directly off the unmanaged shadow stack, leaking adjacent local variables (such as a local `char secret[20]` buffer residing in the same or caller stack frame).
2. Arbitrary linear memory write (`%n`): The `%n` specifier writes the number of bytes output so far to a 32-bit pointer address pulled from the shadow stack. By controlling data on the shadow stack and using width specifiers alongside positional parameters (e.g., `%65536c%2$n`), an attacker can overwrite state variables or pointers at arbitrary offsets within linear memory.

### Testing for Cross-Boundary Integer Truncation and Overflows

A unique class of integer vulnerability occurs at the boundary between JavaScript and WebAssembly due to type representation mismatches. JavaScript represents all numbers as double-precision 64-bit floats (safely representing integers up to `2^53 - 1`), whereas standard WebAssembly `i32` parameters truncate incoming values to 32-bit integers via modulo `2^32` arithmetic (`ToInt32`).

If security checks or array index filters are implemented in JavaScript before calling an exported Wasm function, attackers can bypass the JavaScript check using integer wrap-around:

```javascript
// JavaScript Host Validation
if (index == 1) {
    return "Access Denied: Restricted record";
} else if (index >= 0) {
    // Passes index into Wasm export: char* fetch_record(int index)
    return fetch_record(index);
}
```

To test for cross-boundary integer truncation and internal overflows:

1. JS-to-Wasm truncation bypass: When JavaScript blocks a specific positive integer `N` (such as index `1`) while allowing larger positive numbers, supply `2^32 + N` (for `N = 1`, send `4294967297` / `0x100000001`).
   - In JavaScript: `4294967297 == 1` evaluates to `false`, and `4294967297 >= 0` evaluates to `true`, bypassing the filter.
   - Across the Wasm boundary: The `i32` parameter truncates the upper bits, converting `4294967297` directly into `1` inside the C function and returning the restricted array element (`records[1]`).
2. Allocation size wrap-around: When an exported Wasm function calculates buffer sizes internally (e.g., `malloc(len + 1)` or `malloc(count * 4)`), pass boundary values such as `0xFFFFFFFF` (`-1` / `4294967295`) or `0x40000001` (`1073741825`) to wrap 32-bit multiplication or addition, resulting in an undersized heap allocation followed by an out-of-bounds heap write.

### Analysis Notes and Limitations

- Page-granular trap boundaries: WebAssembly only traps (`RuntimeError: memory access out of bounds`) when a memory read or write crosses the outer limit of allocated 64 KiB pages. Out-of-bounds operations within allocated pages execute silently. Pages added at runtime through `memory.grow` are zero-filled, and bounds checks compare against the current page count rather than the module's declared maximum.
- Emscripten stack cookies: Assertion-enabled Emscripten builds include JavaScript helpers (`writeStackCookie` and `checkStackCookie`) that place magic values (`0x02135467` and `0x89BACDFE`) at the end of the shadow stack, plus a `0x63736d65` (`'emsc'`) sentinel at address `0` when null-write detection (`CHECK_NULL_WRITES`) is enabled. Unlike native per-function stack canaries checked before every `ret` instruction, these cookies are verified at thread startup, at the end of each JavaScript tick, and at program exit (`-sSTACK_OVERFLOW_CHECK=1`); `-sSTACK_OVERFLOW_CHECK=2` additionally instruments every stack-pointer assignment, catching overflows closer to their origin. Intra-frame stack overflows between local variables remain undetected in default builds.
- Signature enforcement on `call_indirect`: Unlike native Return-Oriented Programming (ROP) or Jump-Oriented Programming (JOP), `call_indirect` cannot jump to arbitrary byte offsets. Redirection is strictly restricted to functions listed in `__indirect_function_table` that match the call site's exact parameter and return type signature.
- Residual data in reused heap chunks: Fresh linear memory pages (including pages added by `memory.grow`) are zero-filled, so no information crosses module instances. Within a long-running instance, however, freed chunks retain their contents until overwritten and `malloc` does not zero memory: sensitive data such as tokens, keys, or Personally Identifiable Information (PII) processed in one session can leak to the next user of the same instance, particularly on server-side and edge runtimes. Test by storing a secret, freeing it, reallocating the same size class, and reading the buffer without initializing it.
- Shared memory and threads: Modules built with POSIX threads (`-pthread`) share a single `WebAssembly.Memory` across workers. Bounds checks remain per-access, but check-then-use patterns on shared indices and pointers introduce Time-of-Check to Time-of-Use (TOCTOU) race conditions that can defeat validation performed on the main thread.
- 64-bit linear memory (`memory64`): Engines supporting the `memory64` proposal raise the linear memory index type to 64 bits. Modules compiled against 64-bit memories change the boundary behavior documented in this test case: JavaScript interactions with `i64` values use `BigInt` (`ToBigInt64` rather than `ToInt32` truncation), so 32-bit truncation techniques must be re-evaluated for `i64` boundaries.

## Related Test Cases

- [WebAssembly Reconnaissance (WSTG-WASM-01)](01-WebAssembly_Reconnaissance.md)
- [WebAssembly Static Analysis (WSTG-WASM-02)](02-WebAssembly_Static_Analysis.md)
- [WebAssembly Dynamic Analysis (WSTG-WASM-03)](03-WebAssembly_Dynamic_Analysis.md)
- [Testing for Format String Injection (WSTG-INPV-13)](../11-Injection/12-Format_String_Injection.md)
- [Testing for DOM-Based Cross Site Scripting (WSTG-CLNT-01)](../15-Client-side/01-DOM-based_Cross_Site_Scripting.md)

## Remediation

- Prefer memory-safe languages (such as Rust) when compiling critical components to WebAssembly, and minimize the use of `unsafe` blocks.
- Ensure C/C++ WebAssembly modules are linked with `--stack-first` (in `wasm-ld`) so the downward-growing shadow stack is placed at the beginning of linear memory (below `.data`), ensuring stack underflows immediately hit address `0` and trigger a runtime trap.
- Avoid using inline JavaScript execution macros such as `EM_ASM` or `emscripten_run_script` with buffers residing in linear memory.
- Enforce strict 32-bit integer range validation (`Number.isSafeInteger(x) && x >= 0 && x <= 0x7FFFFFFF`) in JavaScript glue code before passing numeric indices or lengths across the Wasm boundary.
- During testing, build with sanitizer and runtime instrumentation: Emscripten supports AddressSanitizer and UndefinedBehaviorSanitizer (UBSan) via `-fsanitize=address,undefined`, heap access validation (`-sSAFE_HEAP=1`), and stack-cookie verification (`-sSTACK_OVERFLOW_CHECK=1` or `2`, with `-sASSERTIONS=2`). Keep format string warnings (`-Wformat-security`) enabled. Note that `-fsanitize=cfi` is rejected by `emcc` because LLVM Control Flow Integrity (CFI) is not supported for WebAssembly targets; coarse-grained control-flow integrity for indirect calls is instead provided natively by the engine-enforced signature checks on `call_indirect`.
- Calculate allocation sizes with checked arithmetic (`__builtin_add_overflow`, `__builtin_mul_overflow`) before calling `malloc`, and use `calloc` for allocations that must not expose residual linear memory contents.

## Tools

- [WebAssembly Binary Toolkit (WABT)](https://github.com/WebAssembly/wabt) - `wasm-objdump -x` to enumerate the `Elem` section and map `__indirect_function_table` indices for `call_indirect` testing, and `wasm2wat` to inspect layout symbols such as `__stack_low` and `__stack_high`.
- [Owi](https://github.com/OCamlPro/owi) and [SeeWasm](https://github.com/PKU-ASAL/SeeWasm) - Symbolic execution engines capable of automatically generating inputs that trigger out-of-bounds memory accesses, integer overflows, and assertion failures in Wasm binaries.
- [Wasabi](https://github.com/danleh/wasabi) - Dynamic binary instrumentation framework useful for implementing custom runtime bounds checkers and tracking `call_indirect` targets.
- [Binaryen (`wasm-opt`)](https://github.com/WebAssembly/binaryen) - Provides instrumentation passes (such as `--safe-heap`) to detect out-of-bounds heap accesses and null pointer dereferences during testing.

## References

- Lehmann, Kinder, Pradel, ["Everything Old is New Again: Binary Security of WebAssembly"](https://www.usenix.org/system/files/sec20-lehmann.pdf), USENIX Security Symposium, 2020.
- [sola-st/wasm-binary-security](https://github.com/sola-st/wasm-binary-security) - Supplementary artifacts for the USENIX Security 2020 paper, including stack, heap, and global overwrite primitives, end-to-end exploits across browser, Node.js, and Wasmtime runtimes, and static analysis tooling.
- Stiévenart, De Roover, ["Compositional Information Flow Monitoring for WebAssembly"](https://ieeexplore.ieee.org/document/9592405), IEEE EuroS&P, 2021.
- [LLVM WebAssembly lld Port (`--stack-first` documentation)](https://lld.llvm.org/WebAssembly.html)
- [Emscripten Documentation: Debugging and Safe Heap (`SAFE_HEAP`)](https://emscripten.org/docs/porting/Debugging.html)
- [Emscripten Settings Reference (`STACK_OVERFLOW_CHECK`, `SAFE_HEAP`, `CHECK_NULL_WRITES`)](https://emscripten.org/docs/tools_reference/settings_reference.html)
- [Walma: Learning to See Memory Corruption in WebAssembly](https://arxiv.org/html/2603.24167v1) - Machine-learning-based detection of manipulation of Wasm linear memory.
