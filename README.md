# Traducción al español — Pokémon FireRed (gen1recomp)

Mod de traducción al español para **Pokémon FireRed** en
[**gen1recomp**](https://github.com/bryanthaboi/gen1recomp) (motor **0.2.66+**,
que ya soporta los juegos de GBA/Gen 3).

> **Versión del mod:** `v0.1.0`
> **Juego:** Pokémon FireRed

---

### 📍 Hogar del proyecto

Este repositorio es la **casa dedicada** de la traducción de FireRed. Se mantiene
aparte del repo de Gen 1 / Gen 2
([`traduccion-gen1recomp-pokemon-espa-ol`](https://github.com/arcadematicas/traduccion-gen1recomp-pokemon-espa-ol))
porque el **auto-update del gestor de mods** solo admite **un mod por repositorio**
(el gestor, al buscar actualizaciones, cae al primer `.zip` de la release más
nueva; con dos mods en el mismo repo se pisarían).

---

## 📦 Instalación

1. **Descarga** el `.zip` desde *Releases*.
2. **Extrae** el contenido en la carpeta de mods de gen1recomp:
   ```
   <gen1recomp>/.local/share/pokemon-love2d/mods/translation-es-firered/
   ```
   (el zip ya trae la raíz plana: `manifest.json`, `main.lua`, `lang/`).
3. En el **lanzador de mods** de gen1recomp, **activa** `translation-es-firered`.
4. Inicia **Pokémon FireRed**. ✅

El manifest declara `github`, así que el mod **se autoactualiza** desde el gestor
de mods.

## ✅ Cobertura (v0.1.0)

| Catálogo | Entradas | Fuente |
|---|---|---|
| `dialogue` (diálogo de la ROM) | 3464 / 3542 (97,8 %) | corpus oficial EN/ES de FireRed |
| `strings` (texto del motor) | 1871 | reutilizado del mod de Gen 2 |
| `move_names` (movimientos) | 354 | corpus EN/ES |
| `item_names` (objetos) | 307 | corpus EN/ES |
| `item_descriptions` (descripciones) | 306 | corpus oficial EN/ES |

Base: [PokeCorpus](https://github.com/abcboy101/poke-corpus) — corpus paralelo
inglés/español extraído de los propios juegos.

## 📋 Limitaciones conocidas (del motor, no del mod)

No son parcheables por la API de mods actual (se leen directamente de los datos
generados):

- La **intro del Profesor Oak** (`intro/oak_speech.lua`)
- Nombres de **habilidades** (`ability_names.lua`)
- Descripciones de **movimientos y habilidades** (`descriptions.lua`)
- Textos de la **Pokédex** (`dex.lua`)
- ~78 líneas de diálogo sin correspondencia exacta en el corpus

## 🛠️ Regenerar los catálogos

Los catálogos se generan a partir del corpus y de los datos extraídos del ROM.
Estructura del mod:

- `manifest.json` — identidad, juegos y rango de versión del motor
- `main.lua` — registra los overrides/patches (`text`, `strings`, `moves`, `items`)
- `lang/` — los catálogos (esto es todo el trabajo)

## Créditos

- **Fransis** — traducción y adaptación.
- [PokeCorpus](https://github.com/abcboy101/poke-corpus) — textos oficiales.
- [gen1recomp](https://github.com/bryanthaboi/gen1recomp) — motor y sistema de mods.

## Licencia

GPL-3.0 (las traducciones derivan de PokeCorpus, GPL-3.0). Consulta [LICENSE](LICENSE).
