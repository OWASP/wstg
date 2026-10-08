# WebAssembly Reconnaissance

|ID          |
|------------|
|WSTG-WASM-01|

## Summary

WebAssembly (Wasm) is a binary instruction format delivered to the browser as a compiled module. Because it is not human-readable at first glance, it is often wrongly assumed to be protected by "security by obscurity." Just like traditional desktop binaries, WebAssembly modules can be located, fingerprinted, and analyzed.

Reconnaissance is the first step in WebAssembly security testing. This phase focuses on locating Wasm modules within the web application, identifying the toolchain that produced them, checking for exposed debugging artifacts (source maps, DWARF, the `name` section), and mapping the infrastructure attack surface (URLs, API endpoints, hosts) that the modules reveal.

This phase only **collects information** about the target. It deliberately stops before decompiling the code, reading its logic, or running the module under a debugger. Successfully gathering this intelligence provides the foundational map required for the subsequent testing phases.

## Test Objectives

- Find all WebAssembly modules loaded by the target application, including those not named `.wasm`, lazy-loaded, or embedded in JavaScript.
- Identify the compiler toolchain and source language (e.g., C/C++, Rust, Go, .NET) from section metadata, imports, exports, and glue code.
- Detect exposed debugging artifacts: source maps, DWARF information, and the `name` custom section.
- Map the infrastructure attack surface by extracting embedded URLs, API endpoints, and internal hostnames or IP addresses.

## How to Test

### Locating WebAssembly Modules

WebAssembly binaries are loaded by JavaScript, usually asynchronously. The most direct way to discover them is through the browser's developer tools and by inspecting the client-side JavaScript.

#### Browser Developer Tools

1. Open the Developer Tools and go to the **Network** tab.
2. Reload the target application and interact with it so that lazily loaded features are triggered.
3. In Chrome and Edge, select the **Wasm** filter to display only WebAssembly requests. Firefox has no dedicated Wasm filter, so search the request list for `.wasm` and check the content type column for `application/wasm`.
4. Check Web Workers and Service Workers as well. They are common places where Wasm is loaded, and their traffic may appear under separate targets in the DevTools.

#### Inspecting the JavaScript Code

If the application uses lazy loading or bundling, search the JavaScript files for the WebAssembly loading APIs:

- `WebAssembly.instantiate` / `WebAssembly.instantiateStreaming`
- `WebAssembly.compile` / `WebAssembly.compileStreaming`
- `new WebAssembly.Module` / `new WebAssembly.Instance`

Wasm binaries may also be embedded directly in JavaScript to avoid an extra HTTP request. Look for large Base64 strings passed through `atob` or a custom decoder into a `Uint8Array`, and for `data:` URIs such as `data:application/octet-stream;base64,`. Emscripten builds with the `SINGLE_FILE` option do this. Recent Emscripten versions embed the binary with a custom UTF-8 string encoding by default (Base64 is used only if `SINGLE_FILE_BINARY_ENCODE` is disabled), so also look for large string literals that are decoded and passed to the APIs above.

#### Identifying Wasm Files by Content

Do not rely on the file extension or the MIME type alone. Modules may be served as `.bin`, `.dat`, or with no extension, or compressed as `.wasm.gz` or `.wasm.br`. Every Wasm binary starts with the same 8-byte header (the magic bytes `\0asm` followed by the version):

```text
00 61 73 6D 01 00 00 00
```

A downloaded file can be checked with `file module.bin` or `xxd module.bin | head -n 1`. In JavaScript source, the same header appears as the Base64 prefix `AGFzbQ`.

Note that `WebAssembly.instantiateStreaming` and `WebAssembly.compileStreaming` require the server to send the `application/wasm` MIME type, so a Wasm file served with a different type may indicate a server misconfiguration.

### Inspecting Custom Sections

Once a module is downloaded, list its sections with `wasm-objdump` (part of WABT). Most of the remaining reconnaissance steps are answered by this one output:

```sh
wasm-objdump -h module.wasm
```

Look for the following custom sections:

| Section | What it reveals | Covered in |
|---------|-----------------|------------|
| `producers` | Source language and tools used to build the module | Identifying the Compiler and Toolchain |
| `sourceMappingURL` | URL of an external source map | Source Maps |
| `.debug_*`, `external_debug_info` | DWARF debug information, embedded or in a separate file | DWARF Debug Information |
| `name` | Original function and variable names | Name Section |

Custom sections are optional and can be removed at any time. A module with no custom sections at all is common in production builds.

### Identifying the Compiler and Toolchain

Knowing whether a module was compiled from C/C++, Rust, Go, or another language helps the tester understand its memory model, calling conventions, runtime behavior, and expected JavaScript glue code. This information can also help prioritize subsequent security testing. For example, identifying a native-language toolchain may indicate that memory safety, linear-memory handling, unsafe operations, and native-to-JavaScript boundary interactions deserve closer examination, while framework-specific toolchains can point to their corresponding runtime and integration surfaces. Compiler identification should therefore be used to guide test selection and prioritization, not as evidence that a particular vulnerability is present.

#### Automated Detection

Tools such as WASM-Hunter can provide a quick compiler/toolchain identification by scanning the Wasm binary for characteristic strings, symbols, imports, and runtime markers.

```sh
wasm-hunter -compiler -i target_module.wasm
```

Automated identification is heuristic rather than definitive. Optimized, stripped, or obfuscated modules may remove or alter the markers used for detection, so the result should be treated as an initial classification and manually verified when possible.

#### Manual Identification

When automated detection is unavailable or produces an uncertain result, inspect multiple indicators rather than relying on a single signature.

The `producers` custom section is often a useful direct indicator because toolchains may record the languages and tools used to build the module, such as `clang`, `rustc`, or `wasm-bindgen`:

```sh
wasm-objdump -s -j producers module.wasm
```

The `producers` section is optional and is often missing from optimized or hardened builds. In that case, examine the module's imports, exports, runtime strings, associated JavaScript glue code, and surrounding build artifacts. Imports and exports can be listed with `wasm-objdump -x -j Import module.wasm` and `wasm-objdump -x -j Export module.wasm`. Treat individual indicators as hints and, where possible, confirm the identification using a second independent indicator:

- **Emscripten (C/C++):** Imports such as `emscripten_resize_heap`, `__syscall_*`, or `invoke_*`. A generic `env` import module is **not** sufficient evidence because other toolchains use it as well. Release builds usually minify import names (for example, a module named `a`), which hides these patterns.
- **WASI:** An import module such as `wasi_snapshot_preview1` or `wasi_unstable` indicates a build that uses WASI system calls. It does not identify the source language, and Emscripten modules import it too, so additional markers must be checked.
- **Rust (wasm-bindgen):** Imports or exports starting with `__wbindgen_` or `__wbg_`, an import module named `wbg`, and a generated `*_bg.wasm` file next to a `*_bg.js` glue file. The `producers` section typically lists `rustc` and `wasm-bindgen`.
- **Go:** The `wasm_exec.js` glue file, an import module named `gojs` (Go 1.21 and later) or `go` (older releases), and strings such as `runtime.wasmExit`, `runtime.gopanic`, or `Go build ID`. Recent Go versions also add a custom section named `go:buildid`.
- **.NET (Blazor WebAssembly):** A `dotnet.wasm` or `dotnet.native.wasm` file loaded from a `_framework/` path. Before .NET 10, a `blazor.boot.json` manifest is also present. From .NET 10 the boot configuration is inlined into `dotnet.js`.
- **AssemblyScript:** Release builds have almost no markers: typically a single `env.abort` import and a `memory` export. Debug builds keep paths such as `~lib/rt/` in the `name` section, and modules built with `--exportRuntime` export functions like `__new` and `__pin`.

No single marker should be considered conclusive. The strongest identification comes from combining multiple independent indicators, such as `producers` metadata, runtime symbols, imports/exports, glue code, and deployment artifacts.

### Testing for Source Maps and Debugging Symbols

Developers sometimes leave debugging artifacts in production builds. This is a finding by itself, and it also gives the tester a large amount of context.

#### Source Maps

Similar to JavaScript, a WebAssembly module can reference an external source map. The reference is stored in a custom section named `sourceMappingURL`, whose content is the URL of the map file (for example `module.wasm.map`).

If the section is not present, request likely locations such as `module.wasm.map` directly. The JavaScript glue code may also reference its own source map, through a `//# sourceMappingURL=` comment or a `SourceMap` response header. That map describes the JavaScript rather than the module, but it can still expose original source files.

If a map is accessible, open the **Sources** (or **Debugger**) tab in the browser. The browser parses the map and shows the original file layout. How much is recovered depends on the map:

- If the map contains `sourcesContent`, or the referenced source files are downloadable, the original source code can be read.
- Otherwise only file paths and line mappings are recovered, which still reveals project structure, dependency names, and developer paths.

#### DWARF Debug Information

For C, C++, and Rust, debugging data is more commonly shipped as DWARF than as a source map. At the reconnaissance stage, only check whether it is present: either as `.debug_*` sections inside the module, or as an `external_debug_info` section pointing to a separate debug file ("split DWARF") that may be downloadable from the server.

#### Name Section

Even when source maps and DWARF are removed, the `name` custom section is sometimes left in place. It contains the original names of functions and, in some cases, local variables. Check for it in the section listing, and dump it with:

```sh
wasm-objdump -x -j name module.wasm
```

Names from Rust and C++ are usually mangled. Recovered names such as `check_license_key` or `encrypt_password` provide immediate targets for further analysis.

### Attack Surface Mapping (URLs, APIs, and IPs)

WebAssembly modules often contain hardcoded infrastructure details, such as backend API endpoints, absolute URLs, and internal hostnames or IP addresses. Extracting this routing information maps the application's backend architecture.

Testers can extract these assets directly from the compiled binary. For example, `wasm-hunter` can be used to automate this extraction from a local file or a remote URL:

```sh
wasm-hunter -i target_module.wasm
```

(Note: Extracting actual credentials, tokens, and cryptographic keys from the binary is outside the scope of reconnaissance.)

## Related Test Cases

- [Review Web Page Content for Information Leakage (WSTG-INFO-05)](../01-Information_Gathering/05-Review_Web_Page_Content_for_Information_Leakage.md)

## Remediation

- Do not ship source maps, DWARF data, or split debug files to production. Keep debugging and symbol information in a restricted symbol server or other controlled environment.
- Remove unnecessary debugging and build metadata from release builds. For example, `wasm-strip` (WABT) removes all custom sections, and `wasm-opt --strip-debug --strip-producers` (Binaryen) removes debug information and the `producers` section. Configure the compiler and linker to produce stripped release artifacts where supported.
- Do not hardcode internal hostnames, IP addresses, credentials, or sensitive endpoints in client-delivered modules. Treat anything delivered to the browser as public.
- Serve Wasm with the correct `application/wasm` MIME type, and verify that source maps, debug artifacts, and other non-production build files are not publicly accessible.

## Tools

- [WebAssembly Binary Toolkit (WABT)](https://github.com/WebAssembly/wabt) - Includes `wasm-objdump` for listing sections, imports, exports, and names, and `wasm-strip`.
- [WASM-Hunter](https://github.com/Galaxy-sc/WASM-Hunter) - Static analysis tool for Attack Surface Mapping and fast-path compiler detection, with direct remote URL scanning.

## References

- [WebAssembly Specification: Custom Sections and the Name Section](https://webassembly.github.io/spec/core/appendix/custom.html)
- [WebAssembly tool-conventions: Debugging (sourceMappingURL, external_debug_info, DWARF)](https://github.com/WebAssembly/tool-conventions/blob/main/Debugging.md)
- [WebAssembly tool-conventions: Producers Section](https://github.com/WebAssembly/tool-conventions/blob/main/ProducersSection.md)
- [WebAssembly DWARF Debugging Standard](https://yurydelendik.github.io/webassembly-dwarf/)
