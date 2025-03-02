-- Remove all images
function Image(el)
  return {}
end

-- Remove empty spans
-- Remove classes from all spans
function Span(el)
  if #el.content == 0 then
    return {}
  end

  el.classes = pandoc.List{}
  return el
end

-- Unwrap divs
function Div(el)
  return el.content
end

-- Remove raw HTML blocks
function RawBlock(el)
  if el.format == "html" then
    return {}
  end
end

-- Remove raw HTML inlines
function RawInline(el)
  if el.format == "html" then
    return {}
  end
end


-- Remove all links
function Link(el)
  return el.content
end


-- Ensure headers start at level 1
-- Clear all classes from headers
local has_level_1 = false

function Header(el)
  if el.level == 1 then
    has_level_1 = true
  end
  el.classes = pandoc.List{}
  el.attr = pandoc.Attr()
  return el
end

function Pandoc(doc)
  if not has_level_1 then
    return doc:walk {
      Header = function(el)
        if el.level > 1 then
          el.level = el.level - 1
        end
        return el
      end
    }
  end
end

