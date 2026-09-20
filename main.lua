-- translation-es-firered v0.1.0: traducción al español de Pokémon FireRed.
--
-- El motor (gen1recomp >= 0.2.66) expone registros Gen 3:
--   text       -> diálogo de la ROM (IR: lista de comandos)
--   strings    -> texto propio del motor (clave = literal inglés)
--   moves      -> nombres de movimientos (id = nombre inglés normalizado)
--   items      -> nombres y descripciones de objetos (id = nombre inglés normalizado)
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

  local counts = { dialogue = 0, strings = 0, moves = 0, items = 0,
                   itemdesc = 0 }

  -- ---- diálogo de la ROM (Gen 3: valor = lista de comandos IR) ----------
  for key, value in pairs(catalog("dialogue")) do
    if type(value) == "table" and #value > 0 then
      mod.content.text:override(key, value)
      counts.dialogue = counts.dialogue + 1
    end
  end

  -- ---- texto propio del motor ------------------------------------------
  for source, value in pairs(catalog("strings")) do
    if type(source) == "string" and type(value) == "string" and value ~= "" then
      mod.content.strings:override(source, value)
      counts.strings = counts.strings + 1
    end
  end

  -- ---- nombres de movimientos ------------------------------------------
  for id, value in pairs(catalog("move_names")) do
    if type(value) == "string" and value ~= "" then
      mod.content.moves:patch(id, { name = value })
      counts.moves = counts.moves + 1
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
      counts.items = counts.items + 1
      if patch.description then counts.itemdesc = counts.itemdesc + 1 end
    end
  end

  mod.events:on("game.ready", function()
    mod.log:info("Spanish FireRed v0.1.0: %d dialogue, %d strings, %d moves, %d items (%d desc)",
      counts.dialogue, counts.strings, counts.moves, counts.items, counts.itemdesc)
  end)
end
