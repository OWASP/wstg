// OWASP WSTG — Typst entrypoint
//
//   typst compile --root . --input version=4.x .github/ebooks/main.typ out.pdf
//
// Expects /build-ebooks/content.typ (Pandoc body + pandoc-defs + link fixes).

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
#outline(
  title: [Table of Contents],
  depth: 2,
  indent: 1.2em,
)

#pagebreak()

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