# 🇪🇸 Traducción al español — Pokémon FireRed **y LeafGreen**

[![Licencia: GPL-3.0](https://img.shields.io/badge/licencia-GPL--3.0-blue.svg)](LICENSE)
[![Última versión](https://img.shields.io/github/v/release/arcadematicas/traduccion-gen1recomp-firered-es?label=versi%C3%B3n&color=brightgreen)](https://github.com/arcadematicas/traduccion-gen1recomp-firered-es/releases)
[![Gen 3 · GBA](https://img.shields.io/badge/Gen%203-FireRed%20%2B%20LeafGreen-red.svg)](#)
[![gen1recomp 0.3+](https://img.shields.io/badge/gen1recomp-0.3%2B-orange.svg)](https://github.com/bryanthaboi/gen1recomp)

Mod de traducción **al español** de **Pokémon FireRed** y **Pokémon LeafGreen**
para [**gen1recomp**](https://github.com/bryanthaboi/gen1recomp) — el motor que
corre los clásicos de Pokémon (Gen 1, 2 y **3**).

> **Versión:** `v0.2.0` · **Juegos:** FireRed · LeafGreen · **Motor:** gen1recomp 0.3+

---

## ✨ Qué traduce

| Catálogo | | Entradas |
|---|---|:---:|
| 💬 **Diálogos** de la ROM | conversaciones, carteles, escenas | **~11.400** |
| 🖥️ **Textos del motor** | menús, batalla, PC, tiendas, UI | **1824** |
| ⚔️ **Nombres de movimientos** | | **354** |
| 🎒 **Nombres de objetos** | | **307** |
| 📖 **Descripciones de objetos** | | **306** |

Incluye la **intro del Profesor Oak**, y las tablas de texto del motor GBA:
nombres de **clases de entrenador**, nombres de **lugares**, **Fame Checker**,
etiquetas de **menús**, **naturalezas**, **Union Room**, placeholders de
**batalla** (`{B_*}`), etc.

Traducción basada en el [**corpus oficial paralelo EN/ES**](https://github.com/abcboy101/poke-corpus)
extraído de los propios juegos, más el catálogo del motor reutilizado del mod de
Gen 2. Los **acentos y la eñe** funcionan de forma nativa.

## 🚀 Instalación

1. **Descarga** el `.zip` desde [**Releases**](https://github.com/arcadematicas/traduccion-gen1recomp-firered-es/releases).
2. **Extrae** el contenido en la carpeta de mods de gen1recomp:

   ```
   <gen1recomp>/.local/share/pokemon-love2d/mods/translation-es-firered/
   ```

3. En el **lanzador de mods**, activa **`translation-es-firered`** (para FireRed
   y/o LeafGreen).
4. Inicia el juego. 🎮

### 🔄 Autoactualización

El manifest declara el repositorio, así que el gestor de mods **detecta y ofrece
las actualizaciones** automáticamente.

## ⚠️ Limitaciones conocidas

Estas superficies **no son parcheables** con la API de mods actual, así que
quedan en inglés:

- 🧠 **Nombres de habilidades** (`ability_names.lua`)
- 📝 **Descripciones de movimientos y habilidades** (`descriptions.lua`)
- 📕 **Textos de la Pokédex** (`pokemon/pokedex/entries.lua`)
- 🌐 **Easy Chat** (palabras sueltas de Union Room)

## 🗂️ Estructura

```
manifest.json          identidad, juegos y rango de versión del motor
main.lua               registra los overrides/patches (text, strings, moves, items)
lang/
  ├── dialogue.lua           diálogo común FireRed + LeafGreen
  ├── dialogue_firered.lua   diálogo propio/distinto de FireRed
  ├── dialogue_leafgreen.lua diálogo propio/distinto de LeafGreen
  ├── strings.lua            textos del motor (UI)
  ├── move_names.lua
  ├── item_names.lua
  └── item_descriptions.lua
mod.card               ficha del mod
tools/                 pipeline para REGENERAR los catálogos
```

> El diálogo se reparte en tres ficheros porque las claves `g3:*` son
> **direcciones de ROM distintas** en cada juego, y algunas listas de nombres
> (p. ej. las de nombres predefinidos) difieren entre versiones.

### 🛠️ Regenerar la traducción

En [`tools/`](tools/) está el pipeline completo (generadores + validador).
Consulta [`tools/README.md`](tools/README.md).

## 🙏 Créditos

- **Fransis** — traducción y adaptación.
- [**PokeCorpus**](https://github.com/abcboy101/poke-corpus) — textos oficiales.
- [**gen1recomp**](https://github.com/bryanthaboi/gen1recomp) — motor y sistema de mods.

## 📄 Licencia

**GPL-3.0** — las traducciones derivan de PokeCorpus (GPL-3.0). Consulta [LICENSE](LICENSE).

---

<p align="center"><em>Hecho con cariño para que FireRed y LeafGreen se disfruten en español. 🇪🇸</em></p>
