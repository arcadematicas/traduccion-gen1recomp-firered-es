-- Clasifica cada entrada de text.lua: tipos de comando y texto EN reconstruido
local path = arg[1]
local f = io.open(path, "rb")
local data = f:read("*a")
f:close()
local chunk = assert(loadstring(data, path))
local t = chunk()

local function rebuild(cmds)
  local out = {}
  for _, c in ipairs(cmds) do
    local ty = c.t
    if ty == "text" then out[#out+1] = c.s or ""
    elseif ty == "nl" then out[#out+1] = "\\n"
    elseif ty == "para" then out[#out+1] = "\\c"
    elseif ty == "scroll" then out[#out+1] = "\\r"
    elseif ty == "player" then out[#out+1] = "[PLAYER]"
    elseif ty == "rival" then out[#out+1] = "[RIVAL]"
    elseif ty == "strvar" then out[#out+1] = "[STR_VAR_" .. tostring(c.n) .. "]"
    elseif ty == "eos" then
    elseif ty == "ext" then out[#out+1] = "[EXT_" .. tostring(c.n) .. "]"
    elseif ty == "ph" then out[#out+1] = "[PH_" .. tostring(c.n) .. "]"
    else out[#out+1] = "[" .. tostring(ty):upper() .. "]" end
  end
  return table.concat(out)
end

local function typesOf(cmds)
  local seen, order = {}, {}
  for _, c in ipairs(cmds) do
    if not seen[c.t] then seen[c.t] = true; order[#order+1] = c.t end
  end
  table.sort(order)
  return table.concat(order, ",")
end

local keys = {}
for k in pairs(t) do keys[#keys+1] = k end
table.sort(keys)

for _, k in ipairs(keys) do
  local v = t[k]
  if type(v) == "table" then
    io.write(k, "\t", typesOf(v), "\t", rebuild(v), "\n")
  end
end
