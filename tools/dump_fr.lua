-- Reconstruye el texto inglés de cada entrada de text.lua de FireRed
-- y lo vuelca como JSON (clave -> texto reconstruido en formato corpus)
local path = arg[1]
local f = io.open(path, "rb")
local data = f:read("*a")
f:close()
local chunk = assert(loadstring(data, path))
local t = chunk()

local function esc(s)
  s = s:gsub("\\", "\\\\")
  s = s:gsub('"', '\\"')
  s = s:gsub("\n", "\\n")
  s = s:gsub("\r", "\\r")
  s = s:gsub("\t", "\\t")
  s = s:gsub("%c", function(c) return string.format("\\u%04x", c:byte()) end)
  return s
end

-- Reconstruye el texto en formato corpus
local function rebuild(cmds)
  local out = {}
  for _, c in ipairs(cmds) do
    local ty = c.t
    if ty == "text" then
      out[#out+1] = c.s or ""
    elseif ty == "nl" then
      out[#out+1] = "\\n"
    elseif ty == "para" then
      out[#out+1] = "\\c"
    elseif ty == "scroll" then
      out[#out+1] = "\\r"
    elseif ty == "player" then
      out[#out+1] = "[PLAYER]"
    elseif ty == "rival" then
      out[#out+1] = "[RIVAL]"
    elseif ty == "strvar" then
      out[#out+1] = "[STR_VAR_" .. tostring(c.n) .. "]"
    elseif ty == "eos" then
      -- fin
    elseif ty == "ext" then
      out[#out+1] = "[EXT_" .. tostring(c.n) .. "]"
    elseif ty == "ph" then
      out[#out+1] = "[PH_" .. tostring(c.n) .. "]"
    else
      out[#out+1] = "[" .. tostring(ty):upper() .. "]"
    end
  end
  return table.concat(out)
end

local keys = {}
for k in pairs(t) do keys[#keys+1] = k end
table.sort(keys)

local parts = {}
for _, k in ipairs(keys) do
  local v = t[k]
  if type(v) == "table" then
    parts[#parts+1] = string.format('%s\t%s', k, rebuild(v))
  end
end
io.write(table.concat(parts, "\n"))
io.write("\n")
