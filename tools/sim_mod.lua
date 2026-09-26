-- Simula la API de mods del motor 0.3.x y ejecuta main.lua del mod.
local MODDIR = arg[1]
local FAKE_VERSION = arg[2]  -- "firered" | "leafgreen"

local recorded = { text = {}, strings = {}, moves = {}, items = {} }
local function recorder(store)
  return {
    override = function(_, k, v) store[#store+1] = { k = k, v = v } end,
    patch    = function(_, k, v) store[#store+1] = { k = k, v = v } end,
    register = function() end,
  }
end

-- stub de src.core.GameVersion
if FAKE_VERSION then
  package.preload["src.core.GameVersion"] = function()
    return { get = function() return FAKE_VERSION end }
  end
end

local mod = {
  read = function(_, rel)
    local f = io.open(MODDIR .. "/" .. rel, "rb")
    if not f then return nil end
    local b = f:read("*a"); f:close(); return b
  end,
  log = { warn = function(_,...) print("WARN",...) end,
          info = function(_,...) print("INFO",...) end },
  content = { text = recorder(recorded.text), strings = recorder(recorded.strings),
              moves = recorder(recorded.moves), items = recorder(recorded.items) },
  events = { on = function(_, name, fn) if name == "game.ready" then fn() end end },
}

local fn = assert(loadfile(MODDIR .. "/main.lua"))()
fn(mod)

local bad = 0
for _, r in ipairs(recorded.text) do
  local v = r.v
  if type(v) ~= "string" then bad = bad + 1 end
end
print("--- " .. tostring(FAKE_VERSION) .. " ---")
print("text override    :", #recorded.text, "| no-string:", bad)
print("strings override :", #recorded.strings)
print("moves patch      :", #recorded.moves)
print("items patch      :", #recorded.items)
if recorded.text[1] then print("muestra:", recorded.text[1].k, "->", tostring(recorded.text[1].v):sub(1,50)) end
