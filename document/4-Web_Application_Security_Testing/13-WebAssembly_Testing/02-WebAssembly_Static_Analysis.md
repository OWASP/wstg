# WebAssembly Static Analysis

|ID          |
|------------|
|WSTG-WASM-02|

## Summary

Static analysis examines a WebAssembly (Wasm) module without executing it. A Wasm binary has a defined structure made up of standard sections, including types, imports, functions, tables, memory, globals, exports, elements, code, and data. Tooling can display these sections, convert the binary to the WebAssembly text format (WAT), or produce a higher-level representation to help testers understand the module.

This test case focuses on identifying the module's structure and obtaining useful representations of its contents. It covers inspecting standard and custom sections, mapping the module interface, extracting embedded data, and identifying available metadata. While most current browser modules use the core WebAssembly specification, the WebAssembly Component Model is emerging to provide richer interoperability, which may require newer tooling to parse effectively.

This test also describes an optional, controlled client-side modification. This modification helps validate observations about security-sensitive decisions identified during static inspection. It is a limited behavioral check, not proof that a server-side control is absent. Any security finding should be confirmed and reported under the relevant vulnerability-focused test case.

## Test Objectives

- Identify the module format and enumerate its sections.
- Inspect imports, exports, types, functions, tables, memory, globals, element segments, code, and data.
- Convert the binary into readable representations such as WAT, pseudo-code, disassembly, or JavaScript.
- Extract readable strings, data-segment contents, metadata, and available debug information.
- Identify compiler clues and embedded third-party component versions where available.
- Use a controlled modification of a test copy to check whether a security-sensitive decision appears to be enforced only in client-side code.

## How to Test

### Identify the Module and Enumerate Its Sections

Start by confirming that the file is a WebAssembly module. Obtain an overview of its sections using WABT:

```sh
wasm-objdump -h module.wasm
wasm-objdump -x module.wasm
```

The `-h` option displays section headers. The `-x` option displays details about the module's sections. Keep this inventory as a reference. Alternatively, modern tools like `wasm-tools objdump` provide similar structural output.

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

Modules do not always contain every section. Availability depends on the format and features used. Compilers can remove custom sections without changing execution semantics. Production builds typically strip debug and name information.

### Map the Module Interface

Imports and exports describe how a module connects to its host environment. Inspect them with:

```sh
wasm-objdump -x -j Import module.wasm
wasm-objdump -x -j Export module.wasm
```

An export may refer to a function, table, memory, or global. An import identifies an item supplied by the host. Record the import module/name, item kind, export name, and relevant type information. These names provide context but do not guarantee an accurate description of the application's internal logic.

Some toolchains generate recognizable import names. Conversely, Go-compiled modules may expose generic runtime entry points. You can supplement this interface inventory by manually extracting readable strings with `strings`, or by using automated tools like WASM-Hunter to report identified function names:

```sh
wasm-hunter -i module.wasm -funcs-only
```

Treat tool output as an inspection aid rather than a complete functional list. Results depend heavily on retained metadata.

Inspect related structures when needed:

```sh
wasm-objdump -x -j Table module.wasm
wasm-objdump -x -j Elem module.wasm
wasm-objdump -x -j Global module.wasm
wasm-objdump -x -j Memory module.wasm
```

Tables and element segments describe function references and table initialization; read them together. Use these outputs to build a structural inventory. Do not draw vulnerability conclusions from the presence of a section alone.

### Obtain Readable Representations

Different tools provide different views of the same module. Use multiple representations to cross-check observations.

| Tool | Output | Typical use |
|---|---|---|
| `wasm2wat` (WABT) | WebAssembly text format (WAT) | Inspecting sections, instructions, and data in a textual form |
| `wasm-decompile` (WABT) | C-like pseudo-code | Getting a higher-level view of function logic |
| `wasm-objdump -d` (WABT) | Disassembly with byte offsets | Inspecting instructions and locating offsets |
| Browser DevTools | WAT and source maps | Viewing the module's textual representation and source mapping directly in Chrome or Firefox |
| `wasm2js` (Binaryen) | JavaScript representation | Compiling Wasm into readable JavaScript for easier logic analysis |
| `wasm-dis` (Binaryen) | Alternative text representation | Cross-checking output from another tool |
| Ghidra / Radare2 | Disassembly and decompiler view | Navigating larger modules and cross-references |

Example commands:

```sh
wasm2wat module.wasm -o module.wat
wasm-decompile module.wasm -o module.dcmp
wasm-objdump -d module.wasm
wasm2js module.wasm --enable-bulk-memory-opt -o module.js
```

The `wasm2js` tool translates the module into equivalent JavaScript code. This format is highly readable for web testers, but heavily relies on bitwise operations and simulated memory, meaning Static Application Security Testing (SAST) tools may struggle to scan it automatically. Pseudo-code generated by decompilers is an interpretation and may not preserve source-level structure.

If function names are absent, modules rely on indices or generated labels. Use function indices and cross-references when meaningful names are unavailable.

### Inspect Linear Memory and Data Segments

The data section contains initialization data for a module's linear memory. Inspect its structure and extract strings:

```sh
wasm-objdump -x -j Data module.wasm
strings -n 6 module.wasm
```

Use the data-segment offsets to relate data to its location in linear memory. The `strings` utility provides a quick overview but may miss encoded or non-printable data.

Note that some data segments are passive. They are initialized through instructions like `memory.init` (bulk memory operations) rather than being copied automatically at instantiation. Check the segment mode to determine how the module uses the data.

For a broader inventory, tools like WASM-Hunter can automate the extraction of indicators such as URLs, API endpoints, IP addresses, and credential-like strings:

```sh
wasm-hunter -i module.wasm
```

Review automated output alongside the structural data. Extraction is pattern-based and may produce false positives. Record extracted strings as observed artifacts for later validation.

### Inspect Custom Sections and Debug Metadata

Custom sections contain names, compiler metadata, source mapping information, or debug data. Enumerate the sections first:

```sh
wasm-objdump -x module.wasm
```

If DWARF debug information is present, use LLVM's `llvm-dwarfdump` to inspect it:

```sh
llvm-dwarfdump --debug-info module.wasm
```

Look for WebAssembly Source Maps (often a `.wasm.map` file referenced in the binary or loaded by the browser). Source maps allow DevTools to map the Wasm execution directly back to the original C++ or Rust code.

Debug information may include source filenames, directory paths, type information, and variable names. Its absence means source-level context is unavailable, not that the module is unanalyzable.

### Identify Toolchain and Third-Party Component Clues

Static artifacts provide clues about the compiler or bundled dependencies. Search readable strings using `strings` or `wasm-objdump`. For example, Rust builds may retain Cargo registry paths:

```sh
strings -n 6 module.wasm | grep -E 'registry/src/|\.crate'
```

C/C++ libraries may expose version strings or recognizable symbol names. Record these clues with their source and confidence level. Comparing identified components against vulnerability advisories is a separate step covered in dependency testing.

### Review the JavaScript Integration at a Structural Level

When a web application loads the module, locate the JavaScript or TypeScript code that instantiates it (usually `WebAssembly.instantiate` or `WebAssembly.instantiateStreaming`). Record:

- The Wasm file or URL being loaded.
- The import object supplied by the host.
- How the application obtains and calls exported functions.
- How data and buffers pass between JavaScript and Wasm memory.
- Any generated glue code or runtime files.

This step documents the boundary between the module and its host. Deeper analysis of data flow or dangerous sinks belongs in vulnerability-specific test cases.

### Hybrid Analysis: Validating Static Findings via Controlled Module Modification

Static inspection may reveal that a Wasm function determines whether a UI action is enabled. In an authorized assessment, make a small change to a local copy of the module and observe whether the client-side behavior changes. Modifying the browser-side module does not demonstrate a server-side vulnerability.

#### Procedure

1. Identify a specific decision: Use the WAT output, exports, and JavaScript glue code to locate a candidate function. Record the original file hash and preserve an unchanged copy. Trace how the host application uses the function's result.
2. Create an editable representation: Convert the module to WAT using WABT.

   ```sh
   sha256sum module.wasm
   wasm2wat module.wasm -o module.wat
   ```

3. Make one minimal change: Edit only the instruction or data relevant to the hypothesis (e.g., a return value in a client-side decision function). Preserve the function's result types, stack typing, and module invariants.
4. Rebuild and validate the copy:

   ```sh
   wat2wasm module.wat -o module-modified.wasm
   wasm-validate module-modified.wasm
   wasm-objdump -x module-modified.wasm
   sha256sum module-modified.wasm
   ```

   A successful validation confirms format validity, not compatibility with the application.

5. Use the modified copy in the test client: Replace the module response within the permitted test setup using an intercepting proxy (such as Burp Suite's Match and Replace feature or ZAP). Keep the original URL unchanged. Note that Subresource Integrity (SRI) checks, signed manifests, or strict Content Security Policy (CSP) rules can block the loading of modified modules.
6. Compare the observed behavior: Repeat the same action. Record whether the UI changes and whether the application receives a successful or rejected backend response.

#### Interpreting Results

- Client-side behavior changes, but backend rejects: this is consistent with the backend independently enforcing the authorization. Record the client-side weakness only if it has a meaningful impact (e.g., misleading UI).
- Client-side behavior changes and the operation succeeds: do not conclude from the UI alone that server-side authorization was bypassed. Verify the actual application response and document it in the relevant authorization test case.
- Modified module fails to load or behavior does not change: this is inconclusive. Explanations include an invalid edit, integrity checks, caching, or a decision implemented elsewhere.

### Analysis Notes and Limitations

- Static analysis describes the module's structure; it does not establish how the module behaves in every runtime context.
- Names, debug information, and dependency metadata are optional and are often stripped.
- Decompilers and automated extractors provide heuristic findings. Verify important observations against other representations.
- Always record the tool name, version, commands used, and module hash so another tester can reproduce the analysis.

## Related Test Cases

- [WSTG-WASM-01: WebAssembly Reconnaissance](01-WebAssembly_Reconnaissance.md)
- [WSTG-ATHN-04: Testing for Bypassing Authentication Schema](../04-Authentication/04-Bypassing_Authentication_Schema.md)

## Remediation

- Strip debug information, DWARF data, source maps, and unnecessary `name` sections from WebAssembly modules before deploying them to production.
- Minimize exported functions to expose only the interfaces strictly required by the host application.
- Enforce all business logic, authorization, and input validation checks on the server-side. Never rely on client-side WebAssembly to secure sensitive decisions or protect private data.

## Tools

- [WebAssembly Binary Toolkit (WABT)](https://github.com/WebAssembly/wabt) - `wasm-objdump`, `wasm2wat`, `wat2wasm`, `wasm-validate`, and `wasm-decompile`.
- [wasm-tools](https://github.com/bytecodealliance/wasm-tools) - Bytecode Alliance's low-level tooling for manipulating Wasm modules and components.
- [Binaryen](https://github.com/WebAssembly/binaryen) - `wasm-dis` and `wasm2js`.
- [Symbolic Execution Frameworks] - [Owi](https://github.com/OCamlPro/owi) for advanced static and symbolic analysis of Wasm binaries.
- [Online Explorers] - Tools like [WebAssembly Code Explorer](https://anonyco.github.io/WasmFiddlePlusPlus/) or Weave for quick triage without local installations.
- [LLVM](https://llvm.org/docs/CommandGuide/llvm-dwarfdump.html) - `llvm-dwarfdump` for inspecting DWARF debug info.
- [Ghidra WebAssembly plugin](https://github.com/nneonneo/ghidra-wasm-plugin) and [Radare2 / Cutter](https://cutter.re/) - Disassemblers and decompilers supporting Wasm.
- [WASM-Hunter](https://github.com/Galaxy-sc/WASM-Hunter) - Automated extraction of indicators and function names from Wasm modules.

## References

- [WABT `wat2wasm` documentation](https://webassembly.github.io/wabt/doc/wat2wasm.1.html)
- [WebAssembly Specification: Modules](https://webassembly.github.io/spec/core/syntax/modules.html)
- [WebAssembly Component Model](https://component-model.bytecodealliance.org/)
- Lehmann, Kinder, Pradel, ["Everything Old is New Again: Binary Security of WebAssembly"](https://www.usenix.org/system/files/sec20-lehmann.pdf), USENIX Security Symposium, 2020.
