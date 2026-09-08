--[[
  Demote document content headings while preserving chapter H1s.

  Strategy:
    - Synthetic chapter headings (folder-based, marked {.synthetic}) stay at H1
    - Numbered chapter headings (0-6, A-F prefix) stay at H1
    - All other content headings are demoted: H1 → H2, H2 → H3, etc.

  This creates proper nesting: chapters at H1, sections within chapters at H2+.
  Prevents duplicate H1s that would cause excessive page breaks.
]]

function Header(el)
  if el.level < 6 then
    -- Check if this is a synthetic heading (marked with .synthetic class)
    local is_synthetic = false
    for i, class in ipairs(el.classes) do
      if class == "synthetic" then
        is_synthetic = true
        break
      end
    end

    -- Check if heading is a numbered chapter (e.g., "0. Foreword", "3. Framework", "A. History")
    local heading_text = pandoc.utils.stringify(el.content)
    local is_chapter = heading_text:match("^%d+%.%s") or heading_text:match("^[A-F]%.%s")

    -- Don't demote chapters; demote everything else
    if not is_synthetic and not is_chapter then
      el.level = el.level + 1
    end
  end
  return el
end

return { { Header = Header } }
