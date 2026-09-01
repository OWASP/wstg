// OWASP WSTG Typst document template
// Applied via: #show: doc => wstg_template(doc, version: version)
//
// Defines styling for WSTG ebook (PDF/EPUB):
//   - Heading hierarchy with chapter breaks and nesting
//   - OWASP branding colors and fonts
//   - Code/link styling
//   - Table formatting

#let wstg_template(content, version: "4.x") = {
  // ---------------------------------------------------------------------------
  // Page setup
  // ---------------------------------------------------------------------------
  set page(
    paper: "a4",
    margin: (top: 25mm, left: 20mm, bottom: 12mm, right: 20mm),
    header: context {
      set text(size: 8pt, weight: "light", fill: rgb("#004391"))
      set align(right)
      box(
        width: 100%,
        stroke: (bottom: 0.5pt + rgb("#7DC6E9")),
        inset: (bottom: 5pt),
        [
          #box(
            fill: rgb("#D4F2FD"),
            stroke: 0.5pt + rgb("#D4F2FD"),
            radius: 50%,
            inset: (x: 5pt, y: 2pt),
            text(
              size: 7pt,
              fill: rgb("#0080BD"),
              str(counter(page).get().first()),
            ),
          )
          #h(5pt)
          Web Security Testing Guide #version
        ],
      )
    },
    footer: context {
      set text(size: 8pt, fill: luma(120))
      align(center)[OWASP WSTG #version]
    },
  )

  // ---------------------------------------------------------------------------
  // Typography
  // ---------------------------------------------------------------------------
  set text(
    font: "DejaVu Sans",
    size: 11pt,
    lang: "en",
  )

  set par(justify: true, leading: 0.65em)
  set heading(numbering: none)

  show link: it => {
    set text(fill: rgb("#0080BD"))
    it
  }

  show raw.where(block: false): it => {
    box(
      fill: luma(240),
      inset: (x: 3pt, y: 0pt),
      outset: (y: 2pt),
      radius: 2pt,
      it,
    )
  }

  show raw.where(block: true): it => {
    set text(size: 9pt)
    block(
      width: 100%,
      fill: luma(245),
      inset: 8pt,
      radius: 3pt,
      stroke: 0.5pt + luma(220),
      it,
    )
  }

  // Left-align tables (Pandoc centers the 1-column ID tables)
  show table: it => {
    set align(left)
    it
  }

  // ---------------------------------------------------------------------------
  // Headings — page break before each H1 (except Contents)
  // ---------------------------------------------------------------------------
  show heading.where(level: 1): it => {
    if it.label != <contents> {
      pagebreak()
    }
    set text(fill: rgb("#004391"), size: 18pt, weight: "bold")
    set par(leading: 0.9em, hanging-indent: 0em)
    block(above: 0.5em, below: 0.8em, width: 100%, breakable: true, {
      it
      v(0.3em)
      line(length: 100%, stroke: 1pt + rgb("#7DC6E9"))
    })
  }

  show heading.where(level: 2): it => {
    pagebreak(weak: true)
    set text(fill: rgb("#007CBB"), size: 14pt, weight: "bold")
    set par(leading: 0.8em, hanging-indent: 0em)
    block(above: 1.4em, below: 0.5em, width: 100%, breakable: true, it)
  }

  show heading.where(level: 3): it => {
    set text(fill: rgb("#007CBB"), size: 12pt, weight: "bold")
    set par(leading: 0.7em, hanging-indent: 0em)
    block(above: 1.0em, below: 0.4em, width: 100%, breakable: true, it)
  }

  show heading.where(level: 4): it => {
    set text(size: 11pt, weight: "bold")
    block(above: 0.8em, below: 0.3em, it)
  }

  content
}