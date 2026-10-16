# WebAssembly Static Analysis

|ID          |
|------------|
|WSTG-WASM-02|

## Summary

Static analysis examines a WebAssembly (Wasm) module without executing it. A Wasm binary has a defined structure made up of standard sections, including types, imports, functions, tables, memory, globals, exports, elements, code, and data. Tooling can display these sections, convert the binary to the WebAssembly text format (WAT), or produce a higher-level representation to help testers understand the module.

This test case focuses on identifying the module's structure and obtaining useful representations of its contents. It covers inspecting standard and custom sections, mapping the module interface, extracting embedded data, and identifying available metadata. It also describes an optional, controlled client-side modification that can help validate observations about security-sensitive decisions identified during static inspection. This modification is a limited behavioral check, not proof that a server-side control is present or absent; any security finding should be confirmed and reported under the relevant vulnerability-focused test case.

## Test Objectives

- Identify the module format and enumerate its sections.
- Inspect imports, exports, types, functions, tables, memory, globals, element segments, code, and data.
- Convert the binary into readable representations such as WAT, pseudo-code, disassembly, or C output.
- Extract readable strings, data-segment contents, metadata, and available debug information.
- Identify compiler/toolchain clues and embedded third-party component names or versions where available.
- Record the limitations of the available output, including stripped names, missing debug information, and tool-specific coverage.
- Where justified, use a controlled modification of a test copy to check whether a security-sensitive decision appears to be enforced only in client-side code.

## How to Test

### Identify the Module and Enumerate Its Sections

Start by confirming that the file is a WebAssembly module and obtaining an overview of its sections. With WABT, use:

```sh
wasm-objdump -h module.wasm
wasm-objdump -x module.wasm
```

The `-h` option displays section headers. The `-x` option displays details about the module's sections, where supported by the tool and the binary's features. Keep this inventory as a reference for later inspection.

A standard module may contain the following sections:

| Section | What to record |
|---|---|
| Type | Function signatures referenced by imports and defined functions |
| Import | Imported functions and imported tables, memories, or globals |
| Function | Type indices for functions defined in the module |
| Table | Table types and limits |
| Memory | Memory types, limits, and whether memory is imported or defined |
| Global | Global types, mutability, and initializers where shown |
| Export | Names and kinds of items exposed to the host |
| Start | The start function, if present |
| Element | Table initialization and function references |
| Code | Function bodies and instructions |
| Data | Data segments and their initialization information |
| Data Count | Data-segment count metadata, when present |
| Custom | Additional metadata, including a possible `name` section or toolchain-specific information |

Not every module contains every section. Section order and availability depend on the WebAssembly format and features used by the module. Custom sections may be removed without changing the module's execution semantics, and debug or name information may be absent from production builds.

### Map the Module Interface

Imports and exports describe how a module connects to its host environment. Inspect them with:

```sh
wasm-objdump -x -j Import module.wasm
wasm-objdump -x -j Export module.wasm
```

An export may refer to a function, table, memory, or global. An import identifies an item supplied by the host. Record the import module/name, item kind, export name, and relevant type information where available. These names can provide useful context, but they are not guaranteed to describe the application's internal logic.

For example, some toolchains generate recognizable import names or JavaScript bindings. Go-compiled modules may expose generic runtime entry points instead of application-level function names. In such cases, WASM-Hunter can supplement the interface inventory by reporting function names it identifies in the binary:

```sh
wasm-hunter -i module.wasm -funcs-only
```

Treat tool output as an aid to inspection rather than a complete list of all functions. Results depend on the compiler, metadata retained in the module, and the tool's detection logic.

Inspect related structures when needed:

```sh
wasm-objdump -x -j Table module.wasm
wasm-objdump -x -j Elem module.wasm
wasm-objdump -x -j Global module.wasm
wasm-objdump -x -j Memory module.wasm
```

Tables and element segments describe function references and table initialization; they should be read together. The memory section describes memory declarations and limits, while globals records global variables and their types. Use these outputs to build a structural inventory, without drawing vulnerability conclusions from the presence of a section alone.

### Obtain Readable Representations

Different tools provide different views of the same module. Use more than one representation when it helps clarify the structure or cross-check an observation.

| Tool | Output | Typical use |
|---|---|---|
| `wasm2wat` (WABT) | WebAssembly text format (WAT) | Inspecting sections, instructions, and data in a textual form |
| `wasm-decompile` (WABT) | C-like pseudo-code | Getting a higher-level view of function logic |
| `wasm-objdump -d` (WABT) | Disassembly with byte offsets | Inspecting instructions and locating offsets |
| `wasm2js` (Binaryen) | JavaScript representation | Compiling Wasm into readable JavaScript, which is often easier for web security testers to analyze for business logic |
| `wasm-dis` (Binaryen) | Alternative text representation | Cross-checking output from another tool |
| Ghidra with a Wasm loader/plugin | Disassembly and decompiler view | Navigating larger modules and cross-references |

Example commands:

```sh
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm -o module.dcmp
wasm-objdump -d module.wasm
wasm2js module.wasm --enable-bulk-memory-opt -o module.js
```

The exact output and supported options depend on the installed tool version. `wasm2js` translates the module into equivalent JavaScript code, which does not recover the original C, C++, Rust, or Go source code, but provides a highly readable format for web pentesters. Likewise, pseudo-code generated by a decompiler is an interpretation of the binary and may not preserve original names or source-level structure.

If function names are absent, functions may be represented by indices or generated labels. The `name` custom section, if present, can associate indices with names, but it is optional and may be stripped. Continue to use function indices and cross-references when meaningful names are unavailable.

### Inspect Linear Memory and Data Segments

The data section contains initialization data for a module's linear memory. Inspect its structure and extract readable strings:

```sh
wasm-objdump -x -j Data module.wasm
strings -n 6 module.wasm
```

Use the data-segment offsets and lengths shown by the structural output to relate data to its location in linear memory where that information is available. The `strings` utility provides a quick overview of printable sequences in the file, but it does not understand all Wasm section semantics and may not identify encoded, fragmented, or non-printable data.

For a broader automated inventory, WASM-Hunter can extract indicators such as URLs, API endpoints, IP addresses, and credential-like strings from supported data regions:

```sh
wasm-hunter -i module.wasm
```

Review the output alongside the module's section and data-segment information. Automated extraction is pattern-based and may produce false positives or miss values that do not match known formats. Do not treat an extracted string as proof that it is active, sensitive, or security-relevant; record it as an observed artifact for later validation.

Some data segments are passive and are initialized through instructions such as `memory.init` rather than being copied into memory automatically at instantiation. Check the segment mode and the module's instructions when determining how a data segment is used. Readable strings may also be encoded or assembled at runtime, in which case a simple string scan will not reveal their original value.

### Inspect Custom Sections and Debug Metadata

Custom sections may contain names, compiler metadata, source mapping information, or debug data. Enumerate the sections first:

```sh
wasm-objdump -x module.wasm
```

If DWARF debug information is present, LLVM's `llvm-dwarfdump` can help inspect it:

```sh
llvm-dwarfdump --debug-info module.wasm
```

Depending on the build, debug information may include source filenames, directory paths, type information, and variable names. Its absence does not imply that the module cannot be analyzed; it means some source-level context may not be available. The `name` section is also optional, and should not be confused with the module's required import and export interface.

### Identify Toolchain and Third-Party Component Clues

Static artifacts may provide clues about the compiler, build tool, or bundled dependencies. Search readable strings and inspect metadata using tools such as `strings`, `wasm-objdump`, and WASM-Hunter. For example, Rust builds may retain Cargo registry paths or crate names:

```sh
strings -n 6 module.wasm | grep -E 'registry/src/|\.crate'
```

C/C++ libraries may expose version strings, recognizable symbol names, or other identifying data. These clues are not always present, may be misleading, and should be recorded with their source and confidence level. Comparing identified components with vulnerability advisories is a separate assessment step and should be documented in the applicable dependency or vulnerability test case.

### Review the JavaScript Integration at a Structural Level

When the Wasm module is loaded by a web application, locate the JavaScript or TypeScript code that instantiates it, usually through `WebAssembly.instantiate` or `WebAssembly.instantiateStreaming`. Record:

- The Wasm file or URL being loaded.
- The import object supplied by the host.
- How the application obtains and calls exported functions.
- How data and buffers are passed between JavaScript and Wasm memory.
- Any generated glue code or runtime files associated with the module.

This step documents the boundary between the module and its host. Detailed analysis of data flow into browser APIs, dangerous sinks, input validation, or security-sensitive decisions should be performed in the relevant vulnerability-focused test cases.

### Hybrid Analysis: Validating Static Findings via Controlled Module Modification

Static inspection may reveal that a Wasm function determines whether a UI action is enabled, a feature is available, or a client-side workflow proceeds. In an authorized assessment, a tester can make a small change to a local copy of the module and observe whether the client-side behavior changes. This is a supporting experiment: modifying the browser-side module does not, by itself, demonstrate a server-side vulnerability or establish how the server authorizes an operation.

#### Procedure

1. **Identify a specific decision during static analysis.** Use the WAT or decompiler output, function indices, exports, and JavaScript glue code to locate a candidate function. Record the original file hash and preserve an unchanged copy. Do not assume a function is security-sensitive solely because of its name; trace how the host application uses its result.

2. **Create an editable representation.** Use a current WABT build to convert the module to WAT:

   ```sh
   sha256sum module.wasm
   wasm2wat module.wasm -o module.wat
   ```

3. **Make one minimal, documented change.** Edit only the instruction or data relevant to the hypothesis - for example, a return value or conditional branch in a client-side decision function. Preserve the function's result types, stack typing, indices, imports, exports, and other module invariants. This is not source-code recovery: compiled control flow may be difficult to interpret, and a change that looks plausible in WAT may not have the intended meaning.

4. **Rebuild and validate the copy.**

   ```sh
   wat2wasm module.wat -o module-modified.wasm
   wasm-validate module-modified.wasm
   wasm-objdump -x module-modified.wasm
   sha256sum module-modified.wasm
   ```

   If conversion or validation fails, do not treat the output as a usable test artifact. Some modules use features unsupported by an older tool build; use a compatible tool version and record it. A successful validation confirms format/type validity, not compatibility with the application or correctness of the edit.

5. **Use the modified copy in the authorized test client.** Replace the module response only within the permitted test setup - for example, through an intercepting proxy or a local test deployment that supports replacing binary responses. Keep the original URL and host JavaScript behavior unchanged where possible so the test isolates the module change. If the application verifies a module hash, uses a signed manifest, relies on generated glue code, or expects a particular MIME type for streaming compilation, the replacement may be rejected or require additional application-specific setup. Do not change server files or production state as part of this test.

6. **Compare the observed behavior.** Repeat the same client-side action with the original and modified modules. Record whether the UI or local workflow changes, whether the browser reports a compilation/instantiation error, and - if the workflow naturally sends a request - whether the application receives a successful or rejected response. Observing the response is evidence about that tested flow; it does not require modifying the server.

#### Interpreting Results

- **The client-side behavior changes, but the operation is rejected by the application backend:** this is consistent with the backend independently enforcing the operation for that tested request. Record the client-side weakness only if it has a meaningful impact, such as misleading UI or access to client-only functionality; do not claim a server-side bypass.
- **The client-side behavior changes and the operation appears to succeed:** do not conclude from the UI alone that server-side authorization was bypassed. Verify the actual application response and resulting state within the authorized scope, then document the specific request and evidence in the relevant authorization or business-logic test case.
- **The modified module fails to load or the behavior does not change:** this is inconclusive. Possible explanations include an invalid or ineffective edit, a different module instance being loaded, caching, integrity checks, generated JavaScript glue, or a decision implemented elsewhere.

This technique is appropriate only when static analysis identifies a concrete hypothesis worth testing. It should not become a generic attempt to change arbitrary instructions. The goal is to determine whether a client-side decision can be altered and what that change demonstrates about the tested client workflow - not to infer server behavior from the Wasm binary alone.

## Analysis Notes and Limitations

- Static analysis describes the module's structure and the artifacts visible in the binary; it does not establish how the module behaves in every runtime context.
- Names, source paths, debug information, and dependency metadata are optional and may be stripped or transformed during compilation.
- Decompilers and automated extractors provide approximations or heuristic findings. Verify important observations against other representations where possible.
- Compiler and toolchain behavior differs. Do not assume that a method that works for one language or build tool applies to every Wasm module.
- Record the tool name and version, commands used, module hash, relevant output, and any limitations encountered so another tester can reproduce the analysis.

## Tools

- [WebAssembly Binary Toolkit (WABT)](https://github.com/WebAssembly/wabt) - `wasm-objdump`, `wasm2wat`, `wat2wasm`, `wasm-validate`, `wasm-decompile`, and `wasm2c`.
- [Binaryen](https://github.com/WebAssembly/binaryen) - `wasm-dis` for an alternative text representation, `wasm-opt` for module processing, and `wasm2js` for compiling Wasm to JavaScript.
- [LLVM](https://llvm.org/docs/CommandGuide/llvm-dwarfdump.html) - `llvm-dwarfdump` for inspecting DWARF debug information.
- [Ghidra WebAssembly plugin](https://github.com/nneonneo/ghidra-wasm-plugin) - loader, disassembler, and decompiler support for Ghidra; check compatibility with the installed Ghidra version.
- [WASM-Hunter](https://github.com/Galaxy-sc/WASM-Hunter) - automated extraction of function-name clues and indicators such as URLs, endpoints, IP addresses, and credential-like strings from supported Wasm modules.
- `strings` - utility for extracting printable sequences from binary files.

## References

- [WABT `wat2wasm` documentation](https://webassembly.github.io/wabt/doc/wat2wasm.1.html) - converting WAT to a Wasm binary.
- [WABT `wasm-validate` documentation](https://webassembly.github.io/wabt/doc/wasm-validate.1.html) - validating a Wasm binary.
- [WebAssembly Specification: Modules](https://webassembly.github.io/spec/core/syntax/modules.html)
- Lehmann, Kinder, Pradel, ["Everything Old is New Again: Binary Security of WebAssembly"](https://www.usenix.org/system/files/sec20-lehmann.pdf), USENIX Security Symposium, 2020.
- [Emscripten API Reference: emscripten.h](https://emscripten.org/docs/api_reference/emscripten.h.html)
