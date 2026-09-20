-- Simula la API de mods del motor y ejecuta main.lua del mod FireRed.
-- Verifica que main.lua carga, aplica los overrides/patches y no lanza errores.
local MODDIR = arg[1]

local function load_catalog(rel)
  local f = io.open(MODDIR .. "/" .. rel, "rb")
  if not f then return nil end
  local body = f:read("*a"); f:close()
  local chunk = assert(loadstring(body, rel))
  return chunk()
end

local recorded = { text = {}, strings = {}, moves = {}, items = {} }

local function recorder(store)
  return {
    override = function(_, k, v) store[#store+1] = { k = k, v = v } end,
    patch    = function(_, k, v) store[#store+1] = { k = k, v = v } end,
    register = function() end,
  }
end

local mod = {
  read = function(_, rel) return load_catalog(rel) and nil end, -- se parchea abajo
  log = { warn = function(_, ...) print("WARN", ...) end,
          info = function(_, ...) print("INFO", ...) end },
  content = {
    text    = recorder(recorded.text),
    strings = recorder(recorded.strings),
    moves   = recorder(recorded.moves),
    items   = recorder(recorded.items),
  },
  events = { on = function(_, name, fn)
    if name == "game.ready" then fn() end
  end },
}

-- mod:read real
mod.read = function(_, rel)
  local f = io.open(MODDIR .. "/" .. rel, "rb")
  if not f then return nil end
  local b = f:read("*a"); f:close()
  return b
end

local fn = assert(loadfile(MODDIR .. "/main.lua"))()
fn(mod)

local function n(x) local c = 0 for _ in pairs(x) do c = c + 1 end return c end
print("--- Resultados ---")
print("text override    :", #recorded.text)
print("strings override :", #recorded.strings)
print("moves patch      :", #recorded.moves)
print("items patch      :", #recorded.items)

-- Comprobar que los valores de text son listas IR
local bad = 0
for _, r in ipairs(recorded.text) do
  if type(r.v) ~= "table" or r.v[#r.v].t ~= "eos" then bad = bad + 1 end
end
print("text malformados :", bad)

-- Muestras
print("muestra text  :", recorded.text[1] and recorded.text[1].k)
print("muestra move  :", recorded.moves[1] and (recorded.moves[1].k .. " -> " .. tostring(recorded.moves[1].v.name)))
print("muestra item  :", recorded.items[1] and (recorded.items[1].k .. " -> " .. tostring(recorded.items[1].v.name) .. " / " .. tostring(recorded.items[1].v.description and "desc")))
