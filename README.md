# 🇪🇸 Traducción al español — Pokémon FireRed

[![Licencia: GPL-3.0](https://img.shields.io/badge/licencia-GPL--3.0-blue.svg)](LICENSE)
[![Última versión](https://img.shields.io/github/v/release/arcadematicas/traduccion-gen1recomp-firered-es?label=versi%C3%B3n&color=brightgreen)](https://github.com/arcadematicas/traduccion-gen1recomp-firered-es/releases)
[![Gen 3 · GBA](https://img.shields.io/badge/Gen%203-FireRed-red.svg)](#)
[![gen1recomp 0.2.66+](https://img.shields.io/badge/gen1recomp-0.2.66%2B-orange.svg)](https://github.com/bryanthaboi/gen1recomp)

Mod de traducción **al español** de **Pokémon FireRed** para
[**gen1recomp**](https://github.com/bryanthaboi/gen1recomp) — el motor que corre
los clásicos de Pokémon a través de un motor unificado (Gen 1, 2 y **3**).

> **Versión:** `v0.1.0` · **Juego:** Pokémon FireRed · **Motor:** gen1recomp 0.2.66+

---

## ✨ Qué traduce

| Catálogo | | Entradas |
|---|---|:---:|
| 💬 **Diálogos** de la ROM | conversaciones, carteles y escenas | **3464** / 3542 (97,8 %) |
| 🖥️ **Textos del motor** | menús, batalla, PC, tiendas, UI | **1871** |
| ⚔️ **Nombres de movimientos** | | **354** |
| 🎒 **Nombres de objetos** | | **307** |
| 📖 **Descripciones de objetos** | | **306** |

Traducción basada en el
[**corpus oficial paralelo EN/ES**](https://github.com/abcboy101/poke-corpus)
extraído de los propios juegos, más el catálogo del motor reutilizado del mod de
Gen 2. Los **acentos y la eñe** funcionan de forma nativa (la fuente de FRLG del
motor ya incluye los glifos).

## 🚀 Instalación

1. **Descarga** el `.zip` desde [**Releases**](https://github.com/arcadematicas/traduccion-gen1recomp-firered-es/releases).
2. **Extrae** el contenido en la carpeta de mods de gen1recomp:

   ```
   <gen1recomp>/.local/share/pokemon-love2d/mods/translation-es-firered/
   ```

   > El zip ya trae la **raíz plana**: `manifest.json`, `main.lua`, `lang/`.

3. En el **lanzador de mods**, activa **`translation-es-firered`**.
4. Inicia **Pokémon FireRed** y ¡a jugar! 🎮

### 🔄 Autoactualización

El manifest declara el repositorio, así que el gestor de mods **detecta y ofrece
las actualizaciones** automáticamente.

## ⚠️ Limitaciones conocidas

Estas superficies **no son parcheables** con la API de mods actual del motor (se
leen directamente de los datos generados), así que quedan en inglés:

- 🎬 La **intro del Profesor Oak** (`intro/oak_speech.lua`)
- 🧠 **Nombres de habilidades** (`ability_names.lua`)
- 📝 **Descripciones de movimientos y habilidades** (`descriptions.lua`)
- 📕 **Textos de la Pokédex** (`dex.lua`)
- 🔤 ~78 líneas de diálogo sin correspondencia exacta en el corpus

> La intro de Oak podría abordarse con un *hook* aparte (como se hizo en la
> traducción de Gen 2); pendiente para el futuro.

## 🗂️ Estructura

```
manifest.json   identidad, juego y rango de versión del motor
main.lua        registra los overrides/patches (text, strings, moves, items)
lang/           los catálogos — aquí está todo el trabajo
  ├── dialogue.lua            (IR Gen 3: text / nl / para / scroll / player / rival / strvar)
  ├── strings.lua
  ├── move_names.lua
  ├── item_names.lua
  └── item_descriptions.lua
mod.card        ficha del mod (metadatos)
```

## 🙏 Créditos

- **Fransis** — traducción y adaptación.
- [**PokeCorpus**](https://github.com/abcboy101/poke-corpus) — textos oficiales.
- [**gen1recomp**](https://github.com/bryanthaboi/gen1recomp) — motor y sistema de mods.

## 📄 Licencia

**GPL-3.0** — las traducciones derivan de PokeCorpus (GPL-3.0). Consulta [LICENSE](LICENSE).

---

<p align="center"><em>Hecho con cariño para que FireRed se disfrute en español. 🇪🇸</em></p>
