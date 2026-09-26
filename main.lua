-- translation-es-firered v0.2.0: traducción al español de Pokémon FireRed y LeafGreen.
--
-- Gen 3 (motor gen1recomp 0.3.x).  El catálogo de diálogo se reparte así:
--   lang/dialogue.lua           claves idénticas en FireRed y LeafGreen
--   lang/dialogue_firered.lua   claves propias/distintas de FireRed
--   lang/dialogue_leafgreen.lua claves propias/distintas de LeafGreen
-- (las claves g3:* son direcciones de ROM distintas en cada juego, y algunas
--  listas de nombres difieren entre versiones)
--
-- Registros usados:
--   text     -> diálogo (claves de scripts/text.lua; valor = string formato pret)
--   strings  -> texto propio del motor (clave = literal inglés)
--   moves    -> nombres de movimientos (id = nombre inglés normalizado)
--   items    -> nombres y descripciones de objetos (id = nombre inglés normalizado)
return function(mod)
  local function catalog(name)
    local rel = "lang/" .. name .. ".lua"
    local body = mod:read(rel)
    if not body then return {} end
    local chunk, err = loadstring(body, rel)
    if not chunk then
      mod.log:warn("%s has a syntax error: %s", rel, tostring(err))
      return {}
    end
    local ok, table_ = pcall(chunk)
    if not ok or type(table_) ~= "table" then
      mod.log:warn("%s did not return a table: %s", rel, tostring(table_))
      return {}
    end
    return table_
  end

  local counts = { dialogue = 0, strings = 0, moves = 0, items = 0, itemdesc = 0 }
  local function count(key) counts[key] = counts[key] + 1 end

  -- ---- diálogo común + capa por versión --------------------------------
  local function applyDialogue(name)
    for key, value in pairs(catalog(name)) do
      if type(value) == "string" and value ~= "" then
        mod.content.text:override(key, value)
        count("dialogue")
      end
    end
  end
  applyDialogue("dialogue")

  local vid = "firered"
  local okV, GameVersion = pcall(require, "src.core.GameVersion")
  if okV and GameVersion and GameVersion.get then
    vid = GameVersion.get() or vid
  end
  if vid == "leafgreen" then
    applyDialogue("dialogue_leafgreen")
  else
    applyDialogue("dialogue_firered")
  end

  -- ---- texto propio del motor ------------------------------------------
  for source, value in pairs(catalog("strings")) do
    if type(source) == "string" and type(value) == "string" and value ~= "" then
      mod.content.strings:override(source, value)
      count("strings")
    end
  end

  -- ---- nombres de movimientos ------------------------------------------
  for id, value in pairs(catalog("move_names")) do
    if type(value) == "string" and value ~= "" then
      mod.content.moves:patch(id, { name = value })
      count("moves")
    end
  end

  -- ---- objetos: nombre + descripción en un solo patch ------------------
  local item_names = catalog("item_names")
  local item_descs = catalog("item_descriptions")
  local item_ids = {}
  for id in pairs(item_names) do item_ids[id] = true end
  for id in pairs(item_descs) do item_ids[id] = true end
  for id in pairs(item_ids) do
    local patch = {}
    if type(item_names[id]) == "string" then patch.name = item_names[id] end
    if type(item_descs[id]) == "string" then patch.description = item_descs[id] end
    if patch.name or patch.description then
      mod.content.items:patch(id, patch)
      count("items")
      if patch.description then count("itemdesc") end
    end
  end

  mod.events:on("game.ready", function()
    mod.log:info("Spanish FireRed/LeafGreen v0.2.0 [%s]: %d dialogue, %d strings, %d moves, %d items (%d desc)",
      vid, counts.dialogue, counts.strings, counts.moves, counts.items, counts.itemdesc)
  end)
end
