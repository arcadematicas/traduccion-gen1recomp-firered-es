#!/usr/bin/env python3
"""Anade a lang/strings.lua los NOMBRES DE LUGARES (ciudades, rutas, islas...) y
las etiquetas de PLANTA, que el motor dibuja con Strings(nombre ingles).

Fuente ES: corpus FRLG (excluyendo el bloque Easy Chat desalineado).
"""
import re
CORPUS = "/tmp/opencode/poke-corpus/corpus/FireRedLeafGreen"
LG = ("/run/media/fransis/ROMS16TB/batocera/roms/linuxgames/gen1recomp/"
      "gen1recomp-x86_64.AppImage.home/.local/share/pokemon-love2d/leafgreen/"
      "data/generated/gba")
STRINGS = "/tmp/opencode/repo/lang/strings.lua"
EXCLUDE = (7683, 8688)

def load(p):
    with open(p, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]

en = load(CORPUS + "/en_msg.txt")
es = load(CORPUS + "/es_msg.txt")
en2es = {}
for i, (e, s) in enumerate(zip(en, es), start=1):
    if not e or not s or (EXCLUDE[0] <= i <= EXCLUDE[1]):
        continue
    if e not in en2es:
        en2es[e] = s

def lua_escape(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '"': out.append('\\"')
        elif ch == "\\": out.append("\\\\")
        elif ch == "\n": out.append("\\n")
        elif ch == "\t": out.append("\\t")
        elif o < 32 or o == 127: out.append("\\%03d" % o)
        else: out.append(ch)
    return "".join(out)

def lua_unescape(s):
    out=[];i=0
    while i < len(s):
        c = s[i]
        if c == "\\" and i+1 < len(s):
            nx = s[i+1]
            if nx == "n": out.append("\n"); i += 2; continue
            if nx == "t": out.append("\t"); i += 2; continue
            if nx == "\\": out.append("\\"); i += 2; continue
            if nx == '"': out.append('"'); i += 2; continue
            out.append(nx); i += 2; continue
        out.append(c); i += 1
    return "".join(out)

# --- nombres de lugar (secciones de mapa) ---
names = set()
body = open(LG + "/map_sections.lua", encoding="utf-8").read()
names.update(re.findall(r'name = "((?:[^"\\]|\\.)*)"', body))
body = open(LG + "/region_map/names.lua", encoding="utf-8").read()
names.update(re.findall(r'\[\d+\] = "((?:[^"\\]|\\.)*)"', body))
# --- etiquetas de planta ---
floors = set()
for f in ("1F","2F","3F","4F","5F","6F","B1F","B2F","B3F","B4F","ROOFTOP"):
    floors.add(f)

added = {}
missing = []
for n in sorted(names | floors):
    tr = en2es.get(n)
    if tr and tr != n:
        added[n] = tr
    elif n in floors and tr:
        added[n] = tr
    elif tr is None:
        missing.append(n)

# leer strings.lua actual y fusionar
cur = {}
with open(STRINGS, encoding="utf-8") as f:
    body = f.read()
for m in re.finditer(r'\["((?:[^"\\]|\\.)*)"\]\s*=\s*"((?:[^"\\]|\\.)*)"', body):
    cur[lua_unescape(m.group(1))] = lua_unescape(m.group(2))
before = len(cur)
for k, v in added.items():
    cur[k] = v

out = ["-- translation-es-firered · textos propios del motor (registro strings)",
       "-- incluye NOMBRES DE LUGARES (ciudades/rutas/islas) y etiquetas de planta",
       "return {"]
for k in sorted(cur):
    out.append('  ["%s"] = "%s",' % (lua_escape(k), lua_escape(cur[k])))
out.append("}")
with open(STRINGS, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"nombres detectados: {len(names)} | plantas: {len(floors)}")
print(f"strings.lua: {before} -> {len(cur)} (+{len(cur)-before})")
print(f"sin traduccion en el corpus: {len(missing)}")
for m in missing[:20]:
    print("   ", m)
