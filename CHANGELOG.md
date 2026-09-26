# Changelog

Cambios de la traducción al español de **Pokémon FireRed** para
[gen1recomp](https://github.com/bryanthaboi/gen1recomp).

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
la versión vive en `manifest.json`.

---

## [0.2.0] — 2026-09-26

Soporte de **Pokémon LeafGreen** y ampliación masiva del diálogo (motor
gen1recomp **0.3.20**).

### Añadido
- **LeafGreen**: el mod cubre FireRed **y** LeafGreen (`games: [firered, leafgreen]`).
- **Diálogo ampliado**: de ~3.500 a **más de 11.000** cadenas, aprovechando las
  nuevas tablas de texto del motor 0.3.x (clases de entrenador, lugares, Fame
  Checker, etiquetas de menús, naturalezas, Union Room, etc.).
- Nuevo formato de valor del registro `text` (string pret con `{PLAYER}`,
  `{STR_VAR_n}`, tags `{A_BUTTON}`, placeholders `{B_*}`…), que recupera las
  entradas con placeholders de batalla.
- Reparto del diálogo en tres catálogos: `dialogue.lua` (común),
  `dialogue_firered.lua` y `dialogue_leafgreen.lua` (las claves `g3:*` son
  direcciones de ROM distintas por juego).
- Textos del motor actualizados a 0.3.20 (1824 reutilizados).

### Notas
- Pendiente por límites del motor: intro del Prof. Oak, nombres/descripciones de
  habilidades, textos de la Pokédex y palabras de Easy Chat.

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
