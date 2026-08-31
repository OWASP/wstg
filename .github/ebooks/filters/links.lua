--[[
  Rewrite relative .md / directory links into fragment links that match
  Pandoc's auto-generated heading identifiers.
]]

local function slugify(s)
  s = pandoc.utils.stringify(s):lower()
  s = s:gsub("[%s_]+", "-")
  s = s:gsub("[^%w%-]", "")
  s = s:gsub("%-+", "-"):gsub("^%-", ""):gsub("%-$", "")
  return s
end

function Link(el)
  local t = el.target

  -- Leave external links unchanged.
  if t:match("^https?://") or t:match("^mailto:") then
    return nil
  end

  -- Already a fragment.
  if t:match("^#") then
    return nil
  end

  -- Separate an optional fragment from the path.
  local path, frag = t:match("^(.-)#(.+)$")
  if not path then
    path, frag = t, nil
  end

  -- Drop directories / trailing slash; strip Markdown extension.
  local base = path:gsub("/$", ""):match("([^/]+)$") or path
  base = base:gsub("%.md$", ""):gsub("%.markdown$", "")

  -- README / empty -> use parent folder name if present.
  if base == "" or base:lower() == "readme" then
    local parent = path:gsub("/$", ""):match("([^/]+)/[^/]*$")
    if parent then
      base = parent
    end
  end

  -- Drop leading chapter numbering:
  --   0-Foreword              -> Foreword
  --   4.1.1-Testing_Foo       -> Testing_Foo
  base = base:gsub("^[%d%.]+%-", "")

  -- Drop leading appendix lettering:
  --   A-Testing_Tools_Resource -> Testing_Tools_Resource
  --   B-Suggested_Reading      -> Suggested_Reading
  --
  -- Use any single alphabetic prefix rather than hard-coding A-F so
  -- future appendices continue to work.
  base = base:gsub("^%a%-", "")

  local id = frag and slugify(frag) or slugify(base)

  el.target = "#" .. id
  return el
end

return {
  {
    Link = Link
  }
}
