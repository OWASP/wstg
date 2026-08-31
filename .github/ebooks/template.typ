#let wstg_template(content, version: "4.x") = {
  set page(
    paper: "a4",
    margin: (top: 25mm, left: 20mm, bottom: 10mm, right: 20mm),
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
            text(size: 7pt, fill: rgb("#0080BD"), str(counter(page).get().first()))
          )
          #h(5pt)
          Web Security Testing Guide #version
        ]
      )
    },
  )

  set text(
    font: ("New Computer Modern", "Liberation Sans", "DejaVu Sans"),
    size: 11pt,
  )

  show heading.where(level: 1): it => {
    set text(fill: rgb("#004391"), size: 18pt)
    block(above: 2em, below: 1em, it)
  }
  show heading.where(level: 2): it => {
    set text(fill: rgb("#007CBB"), size: 14pt)
    block(above: 1.5em, below: 0.5em, it)
  }
  show heading.where(level: 3): it => {
    set text(fill: rgb("#007CBB"), size: 12pt)
    block(above: 1em, below: 0.5em, it)
  }

  content
}
