#import "/.github/ebooks/template.typ": wstg_template

// Passed from CI: typst compile --input version=4.x ...
#let version = sys.inputs.at("version", default: "dev")

// Front covers (paths are root-absolute; compile with --root <repo>)
#page(margin: 0pt)[
  #set align(center + horizon)
  #image("/.github/pdf/assets/cover.jpg", width: 100%, height: 100%, fit: "cover")
]

#page(margin: 0pt)[
  #set align(center + horizon)
  #image("/.github/pdf/assets/second-cover.png", width: 100%, height: 100%, fit: "cover")
]

#show: doc => wstg_template(doc, version: version)

// Pandoc writes this in the build dir; path is still under --root
#include "/build-ebooks/content.typ"

#page(margin: 0pt)[
  #set align(center + horizon)
  #image("/.github/pdf/assets/back-cover.png", width: 100%, height: 100%, fit: "cover")
]