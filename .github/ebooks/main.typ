// OWASP WSTG — Typst entrypoint for ebook generation
//
// Assembles the complete ebook:
//   1. Front matter (cover images)
//   2. Table of contents (from heading structure)
//   3. Content body (from Pandoc-generated content.typ)
//   4. Back cover
//
// Expects /build-ebooks/content.typ (Pandoc output with link/style fixes)
//
// Build: typst compile --root . --input version=4.x .github/ebooks/main.typ out.pdf

#import "/.github/ebooks/template.typ": wstg_template

#let version = sys.inputs.at("version", default: "dev")

// ---------------------------------------------------------------------------
// Front cover
// ---------------------------------------------------------------------------
#page(margin: 0pt)[
  #set align(center + horizon)
  #image(
    "/.github/pdf/assets/cover.jpg",
    width: 100%,
    height: 100%,
    fit: "cover",
  )
]

// ---------------------------------------------------------------------------
// Second cover / frontispiece
// ---------------------------------------------------------------------------
#page(margin: 0pt)[
  #set align(center + horizon)
  #image(
    "/.github/pdf/assets/second-cover.png",
    width: 100%,
    height: 100%,
    fit: "cover",
  )
]

// ---------------------------------------------------------------------------
// Body
// ---------------------------------------------------------------------------
#show: doc => wstg_template(doc, version: version)

// Clickable PDF outline from heading structure (prefer over path-based MD ToC)
= Contents <contents>

#outline(
  title: none,
  depth: 2,
  indent: 2em,
)

#include "/build-ebooks/content.typ"

// ---------------------------------------------------------------------------
// Back cover
// ---------------------------------------------------------------------------
#page(margin: 0pt)[
  #set align(center + horizon)
  #image(
    "/.github/pdf/assets/back-cover.png",
    width: 100%,
    height: 100%,
    fit: "cover",
  )
]