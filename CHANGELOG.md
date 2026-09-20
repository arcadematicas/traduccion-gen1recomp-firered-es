# Changelog

Cambios de la traducción al español de **Pokémon FireRed** para
[gen1recomp](https://github.com/bryanthaboi/gen1recomp).

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
la versión vive en `manifest.json`.

---

## [0.1.0] — 2026-09-20

Primera versión publicada. Traducción de Pokémon FireRed (Gen 3) con el motor
gen1recomp 0.2.66+.

### Añadido
- **3464/3542 diálogos** de la ROM traducidos (97,8 %), desde el corpus oficial
  paralelo EN/ES de FireRed/LeafGreen, convertidos a la forma IR del motor Gen 3
  (`text`/`nl`/`para`/`scroll`/`player`/`rival`/`strvar`).
- **1871 cadenas del motor** (textos de UI) reutilizadas del catálogo de Gen 2.
- **354 nombres de movimientos** y **307 nombres de objetos** (id = nombre inglés
  normalizado con `G3.idOf`).
- **306 descripciones de objetos** traducidas.
- Acentos y eñe soportados de forma nativa por la fuente de FRLG del motor.

### Notas
- Auto-update habilitado (`github` en el manifest).
- Pendiente por límites del motor: intro del Prof. Oak, nombres de habilidades,
  descripciones de movimientos/habilidades y textos de la Pokédex.
