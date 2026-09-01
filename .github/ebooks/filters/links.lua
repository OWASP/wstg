--[[
  Resolve relative Markdown links to fragment identifiers for ebook navigation.

  Converts links like [text](../some-chapter/file.md#anchor) to [text](<fragment>)
  for use in Typst/EPUB where cross-chapter links must be to heading IDs.

  Resolution strategy (in order):
    1. If link has explicit fragment (after #), slugify it and use as-is
    2. Try manifest lookup: find exact heading ID from AST (built by build-link-manifest.py)
    3. Fall back to regex-guessing: slugify filename or directory name

  The manifest eliminates fragile "filename must match heading" assumptions
  by using Pandoc's actual AST-derived identifiers.

  Manifest lookup requires LINK_MANIFEST env var pointing to link-manifest.json.
]]

local manifest = {}
local manifest_loaded = false

local function slugify(s)
  s = pandoc.utils.stringify(s):lower()
  s = s:gsub("[%s_]+", "-")
  s = s:gsub("[^%w%-]", "")
  s = s:gsub("%-+", "-"):gsub("^%-", ""):gsub("%-$", "")
  return s
end

local function load_manifest(path)
  if manifest_loaded then return end
  manifest_loaded = true

  local f = io.open(path, "r")
  if not f then return end

  local content = f:read("*a")
  f:close()

  local ok, result = pcall(function() return pandoc.json.decode(content) end)
  if ok and result then
    manifest = result
  end
end

local function resolve_link(target, frag)
  --[[
    Given a target file (relative path, .md/.markdown optional) and optional fragment,
    resolve to the real heading id.
    First tries manifest; falls back to slugifying the fragment or target.
  ]]

  -- If fragment is explicit, use it.
  if frag then
    return slugify(frag)
  end

  -- Normalize target: strip .md/.markdown, trailing slash.
  target = target:gsub("/$", ""):gsub("%.md$", ""):gsub("%.markdown$", "")

  -- Infer filename from path: "dir/file" -> "file", "dir" -> "dir".
  local base = target:match("([^/]+)$") or target

  -- Special case: README or empty -> use parent folder name.
  if base == "" or base:lower() == "readme" then
    local parent = target:match("([^/]+)/[^/]*$")
    if parent then
      base = parent
    end
  end

  local base_slug = slugify(base)

  -- Try manifest: look for a file matching the target path.
  for filepath, headings in pairs(manifest) do
    -- Normalize manifest filepath for comparison.
    local manifest_file = filepath:gsub("%.md$", ""):gsub("%.markdown$", "")

    -- Check if this manifest file matches the target.
    if manifest_file == target or manifest_file:match(target .. "$") then
      if headings[base_slug] then
        return headings[base_slug]
      end
      -- If file found but heading slug not found, fall through to fallback.
      break
    end
  end

  -- Fall back to regex-based slug derivation (old behavior).
  base = base:gsub("^[%d%.]+%-", "")
  base = base:gsub("^%a%-", "")
  return slugify(base)
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

  -- Load manifest on first link (lazy load).
  if not manifest_loaded then
    local manifest_path = os.getenv("LINK_MANIFEST") or "build-ebooks/link-manifest.json"
    load_manifest(manifest_path)
  end

  -- Separate optional fragment from path.
  local path, frag = t:match("^(.-)#(.+)$")
  if not path then
    path, frag = t, nil
  end

  local id = resolve_link(path, frag)
  el.target = "#" .. id
  return el
end

return {
  {
    Link = Link
  }
}
