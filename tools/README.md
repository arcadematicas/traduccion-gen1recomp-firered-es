# 🛠️ tools — regenerar los catálogos de la traducción (FireRed + LeafGreen)

Pipeline para reconstruir `lang/` a partir del corpus oficial y de los datos
extraídos del ROM. **No forma parte del mod** (no hace falta para jugar).

## 📥 Entradas necesarias

| Qué | Dónde |
|---|---|
| Corpus FireRed/LeafGreen (EN↔ES, alineado) | [`abcboy101/poke-corpus`](https://github.com/abcboy101/poke-corpus) → `corpus/FireRedLeafGreen/{en_msg.txt,es_msg.txt}` |
| Corpus XY (EN↔ES, nombres de movs/objetos) | `corpus/XY/{en_common.txt,es_common.txt}` |
| Datos del ROM (FireRed y LeafGreen) | `<gen1recomp>/.local/share/pokemon-love2d/{firered,leafgreen}/data/generated/gba/` |
| Fuente del motor 0.3.x | extraer `src/` del `.love` |
| Catálogo ES del mod de Gen 2 (strings del motor) | `.../mods/translation-es-goldilvercrystal/lang/strings.lua` |

Necesitas `luajit`, `python3` y `zip`.

## 🔄 Pipeline

```bash
# 0) Extraer el motor
mkdir -p engine && cd engine && unzip -q /ruta/gen1recomp-0.3.XX.love

FR=<...>/firered/data/generated/gba
LG=<...>/leafgreen/data/generated/gba

# 1) Del ROM -> tablas de trabajo (por juego)
luajit tools/classify_text.lua "$FR/scripts/text.lua" > fr_new.tsv
luajit tools/classify_text.lua "$LG/scripts/text.lua" > lg_new.tsv
luajit tools/ex_names.lua "$FR/pokemon/move_names.lua" "$FR/pokemon/ability_names.lua" \
                          "$FR/items/pack.lua" > fr_names.tsv
luajit tools/ex_items.lua "$FR/items/pack.lua" > fr_items.tsv

# 2) Strings del motor
python3 tools/harvest_strings.py engine/src > engine_strings.txt

# 3) Generar los catálogos -> lang/
python3 tools/gen_dialogue.py    # corpus + fr_new.tsv/lg_new.tsv -> dialogue{,_firered,_leafgreen}.lua
python3 tools/gen_strings.py     # engine_strings.txt + GSC -> strings.lua
python3 tools/gen_names.py       # corpus XY + FRLG -> move_names/item_names/item_descriptions.lua

# 4) Validar
luajit tools/sim_mod.lua <carpeta_del_mod> firered
luajit tools/sim_mod.lua <carpeta_del_mod> leafgreen
```

> Las rutas esperadas están en las constantes de cabecera de cada script; ajústalas
> si trabajas en otro equipo. `classify_text.lua` usa `loadstring` (LuaJIT), no `loadfile`.

## 🧩 Formato del diálogo (clave en 0.3.x)

El registro `text` acepta:
- **lista IR** (`{t="text",s=...}`, `{t="nl"}`, `{t="para"}`, …), o
- **string**, que el motor pasa por `TextIR.fromAscii` si contiene `[`, `{` o `\`.

El generador emite **strings en formato pret**:
`{PLAYER}`, `{RIVAL}`, `{STR_VAR_n}`, `\n` (salto), `\p` (párrafo), `\l` (scroll),
tags `{A_BUTTON}`/`{PKMN}`/`{FONT_*}`, placeholders de batalla `{B_*}`.

Conversión desde el corpus: `[PLAYER]`→`{PLAYER}`, `\c`→`\p`, `\r`→`\l`,
`[B_*]`→`{B_*}`, `[TAG]`→`{TAG}`.

## 🗂️ Reparto del diálogo

- `dialogue.lua` — claves idénticas en FireRed y LeafGreen.
- `dialogue_firered.lua` / `dialogue_leafgreen.lua` — claves propias o distintas
  (las `g3:*` son direcciones de ROM diferentes por juego; algunas listas de
  nombres también cambian).

`main.lua` aplica la común y, según `GameVersion.get()`, la del juego en curso.

## 📌 Notas de la API Gen 3

- `mod.content.text:override(clave, valor)` — `scripts/text.lua`.
- `mod.content.strings:override(literalInglés, traducción)` — registro global.
- `mod.content.moves:patch(id, {name=…})` / `items:patch(id, {name=…, description=…})`
  — **id = nombre inglés normalizado con `G3.idOf`** (no el índice numérico).
- **No parcheables**: intro de Oak (`intro/oak_speech.lua`), nombres de habilidades
  (`ability_names.lua`), descripciones (`descriptions.lua`), Pokédex
  (`pokemon/pokedex/entries.lua`), Easy Chat (`easy_chat/words.lua`).

## ⚙️ `enable_firered.py`

Activa el mod en `options.lua` añadiendo el bucket de la versión. En 0.3.x el
estado de mods activos también se guarda **en la partida** (`saves/<juego>/slotN.lua`),
así que lo normal es activarlo desde el lanzador de mods del juego.
