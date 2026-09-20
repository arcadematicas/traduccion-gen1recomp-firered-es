# 🛠️ tools — regenerar los catálogos de la traducción

Este directorio contiene el *pipeline* con el que se generan los catálogos de
`lang/` a partir de los datos del ROM y del corpus oficial. **No forma parte del
mod** (no hace falta para jugar); solo se usa para regenerar/actualizar.

## 📥 Entradas necesarias

| Qué | Dónde se obtiene |
|---|---|
| **Corpus FireRed/LeafGreen** (EN↔ES, 14479 líneas alineadas) | [`abcboy101/poke-corpus`](https://github.com/abcboy101/poke-corpus) → `corpus/FireRedLeafGreen/{en_msg.txt,es_msg.txt}` |
| **Corpus XY** (EN↔ES, para *nombres* de movimientos/objetos) | `corpus/XY/{en_common.txt,es_common.txt}` |
| **Datos del ROM de FireRed** (extraídos por gen1recomp) | `<gen1recomp>/.local/share/pokemon-love2d/firered/data/generated/gba/` |
| **Fuente del motor** (para los textos de UI) | extraer `src/` del `.love` de gen1recomp (es un zip) |
| **Catálogo ES del mod de Gen 2** (reutilización de strings del motor) | `.../mods/translation-es-goldilvercrystal/lang/strings.lua` |

Utilidades: `luajit`, `python3`, `zip`.

## 🔄 Pipeline

```bash
# 0) Extraer el motor del .love (una vez por versión)
mkdir -p engine && cd engine && unzip -q /ruta/gen1recomp-X.Y.Z.love

# 1) Del ROM de FireRed -> tablas de trabajo (luajit)
FR=<...>/firered/data/generated/gba
luajit tools/classify_fr.lua  "$FR/scripts/text.lua"        > fr_class.tsv   # clave<TAB>tipos<TAB>EN
luajit tools/dump_fr.lua      "$FR/scripts/text.lua"        > fr_en.tsv
luajit tools/ex_names.lua     "$FR/pokemon/move_names.lua" \
                              "$FR/pokemon/ability_names.lua" \
                              "$FR/items/pack.lua"          > fr_names.tsv   # KIND<TAB>num<TAB>nombre
luajit tools/ex_items.lua     "$FR/items/pack.lua"          > fr_items.tsv   # num<TAB>nombre<TAB>descripción EN
luajit tools/ex_desc.lua      "$FR/items/pack.lua" \
                              "$FR/pokemon/descriptions.lua" > fr_desc.tsv

# 2) Del fuente del motor -> literales de UI
python3 tools/harvest_strings.py engine/src                 > engine_strings.txt

# 3) Generar los catálogos -> lang/
python3 tools/gen_dialogue.py       # corpus FRLG + fr_class.tsv  -> lang/dialogue.lua (IR Gen3)
python3 tools/gen_strings.py        # engine_strings.txt + GSC    -> lang/strings.lua
python3 tools/gen_names.py          # corpus XY + FRLG + tablas   -> move_names/item_names/item_descriptions.lua

# 4) Validar
luajit tools/sim_mod.lua <carpeta_del_mod>   # simula la API de mods y aplica todo
```

> Nota: `gen_*.py` llevan las rutas esperadas en sus constantes de cabecera;
> ajústalas si trabajas en otro equipo. `dump_fr.lua`/`classify_fr.lua` usan
> `loadstring` (LuaJIT), no `loadfile`.

## 🧪 `sim_mod.lua`

Simula el motor (registros `text`/`strings`/`moves`/`items`) y ejecuta el
`main.lua` del mod, comprobando:

- que `main.lua` carga y no lanza errores,
- que los valores de `text` son listas IR válidas (terminan en `{t="eos"}`),
- cuántos overrides/patches se aplican de cada tipo.

## ⚙️ `enable_firered.py`

Activa el mod en `options.lua` (añade el bucket `firered` en `modsByVersion` y
`enabledByVersion`) y hace copia de seguridad. Normalmente **no hace falta**: el
lanzador de mods del juego permite activarlo a mano.

## 📌 Notas de la API Gen 3 (importante al tocar los generadores)

- `mod.content.text:override(clave, ir)` — `ir` es una **lista de comandos**:
  `{t="text",s=...}`, `{t="nl"}`, `{t="para"}`, `{t="scroll"}`, `{t="player"}`,
  `{t="rival"}`, `{t="strvar",n=1|2|3}`, `{t="eos"}`.
  Claves = las de `scripts/text.lua` (`Text_*` o `["g3:DIR"]`).
- Conversión corpus ES → IR: `\n`→nl, `\c`→para, `\r`→scroll, `[PLAYER]`→player,
  `[RIVAL]`→rival, `[STR_VAR_n]`→strvar n, `[SUPER_ER]`→`"º"`.
- `mod.content.moves:patch(id, {...})` / `items:patch(id, {...})` — **id = nombre
  inglés normalizado con `G3.idOf`** (é→E, ♀→_F, ♂→_M, quita `'`, `upper`,
  no-`%w`→`_`), **no** el índice numérico.
- `mod.content.strings:override(literalInglés, traducción)` — registro global.
- **No parcheables** (se leen directos): intro de Oak (`intro/oak_speech.lua`),
  nombres de habilidades (`ability_names.lua`), descripciones (`descriptions.lua`),
  texto de Pokédex (`dex.lua`).
