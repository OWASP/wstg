--[[
  Convert single-column ID tables (WSTG-…) into styled callout badges for Typst.
  For other formats (EPUB, HTML), preserve the original table.
]]

function Table(tbl)
  local function cell_text(c)
    return pandoc.utils.stringify(c)
  end

  -- Match: | ID |
  --        |----|
  --        | WSTG-… |
  if tbl.headers and #tbl.headers == 1
     and cell_text(tbl.headers[1]):match("^ID") then
    local body = tbl.bodies and tbl.bodies[1]
    if body and body.body and #body.body == 1 then
      local id = cell_text(body.body[1][1])
      if id:match("^WSTG%-") then
        local typst = string.format([[
#block(
  fill: rgb("#D4F2FD"),
  stroke: 1pt + rgb("#0080BD"),
  radius: 4pt,
  inset: 8pt,
  width: auto,
)[
  *ID* #h(0.75em) `%s`
]
]], id)
        return pandoc.RawBlock("typst", typst)
      end
    end
  end
  -- Return nil to keep original table for non-Typst formats
  return nil
end

return { { Table = Table } }
