#!/usr/bin/env python3
"""Genera move_names.lua, item_names.lua e item_descriptions.lua para FireRed.

Los registros gen3 indexan por el nombre inglés NORMALIZADO con G3.idOf, no por
el índice numérico. Este script computa ese id.
"""
import re

FR = ("/run/media/fransis/ROMS16TB/batocera/roms/linuxgames/gen1recomp/"
      "gen1recomp-x86_64.AppImage.home/.local/share/pokemon-love2d/firered/"
      "data/generated/gba")
MOD = "/tmp/opencode/repo/translation-es-firered/lang"


def g3_id_of(name):
    """Réplica de G3.idOf de Schemas.lua."""
    s = name.replace("é", "E").replace("É", "E")
    s = s.replace("♀", "_F").replace("♂", "_M")
    s = s.replace("'", "")
    s = s.upper()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s)
    s = s.strip("_")
    return s


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_pairs(en_path, es_path):
    with open(en_path, encoding="utf-8") as f:
        en = [l.rstrip("\n") for l in f]
    with open(es_path, encoding="utf-8") as f:
        es = [l.rstrip("\n") for l in f]
    d = {}
    for e, s in zip(en, es):
        k = norm(e)
        if k and k not in d:
            d[k] = s
    return d


def lua_escape(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif o < 32 or o == 127:
            out.append("\\%03d" % o)
        else:
            out.append(ch)
    return "".join(out)


def parse_tsv_names(path):
    moves, items = {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            kind, num, name = p[0], p[1], p[2]
            if kind == "MOVE":
                moves[int(num)] = name
            elif kind == "ITEM":
                items[int(num)] = name
    return moves, items


MOVE_OVERRIDES = {
    "HI JUMP KICK": "PATADA SALTO ALTA",
    "FAINT ATTACK": "FINTA",
    "SMELLINGSALT": "ESTÍMULO",
}
ITEM_OVERRIDES = {
    "X SPECIAL": "ESPECIAL X",
    "X DEFEND": "DEFENSA X",
    "PARLYZ HEAL": "ANTIPARALIZADOR",
    "RUBY": "RUBÍ",
    "SAPPHIRE": "ZAFIRO",
    "TEA": "TÉ",
    "TRI-PASS": "TRI-PASE",
    "RAINBOW PASS": "PASE ARCOÍRIS",
    "AURORATICKET": "TICKET AURORA",
    "MYSTICTICKET": "TICKET MÍSTICO",
    "TM CASE": "CAJA MT",
    "BERRY POUCH": "BOLSA BAYA",
    "POWDER JAR": "FRASCO POLVO",
    "ORANGE MAIL": "CARTA NARANJA",
    "HARBOR MAIL": "CARTA PUERTO",
    "GLITTER MAIL": "CARTA BRILLO",
    "MECH MAIL": "CARTA MECÁNICA",
    "WOOD MAIL": "CARTA MADERA",
    "WAVE MAIL": "CARTA OLAS",
    "BEAD MAIL": "CARTA PERLAS",
    "SHADOW MAIL": "CARTA SOMBRA",
    "TROPIC MAIL": "CARTA TRÓPICO",
    "DREAM MAIL": "CARTA SUEÑO",
    "FAB MAIL": "CARTA FANTASÍA",
    "RETRO MAIL": "CARTA RETRO",
    "MACH BIKE": "BICI CARRERA",
    "ACRO BIKE": "BICI ACROBÁTICA",
    "ITEMFINDER": "ZAHORÍ",
    "WAILMER PAIL": "REGADERA WAILMER",
    "DEVON GOODS": "PIEZAS DEVON",
    "SOOT SACK": "SACO DE CENIZA",
    " CASE": "ESTUCHE",
    "LETTER": "CARTA",
    "EON TICKET": "TICKET EÓN",
    "SCANNER": "ESCÁNER",
    "GO-GOGGLES": "GAFAS AISLANTES",
    "METEORITE": "METEORITO",
    "RM. 1 KEY": "LLAVE SALA 1",
    "RM. 2 KEY": "LLAVE SALA 2",
    "RM. 4 KEY": "LLAVE SALA 4",
    "RM. 6 KEY": "LLAVE SALA 6",
    "DEVON SCOPE": "SCOPE DEVON",
    "HM07": "MO07",
    "HM08": "MO08",
    "OAK'S PARCEL": "PAQUETE DE OAK",
    "BIKE VOUCHER": "BONO BICI",
    "GOLD TEETH": "DIENTES DE ORO",
    "LIFT KEY": "LLAVE ASCENSOR",
    "SILPH SCOPE": "SCOPE SILPH",
    "FAME CHECKER": "FAMOSOS",
}


def write_catalog(path, mapping, header):
    lines = [header, "return {"]
    for key in sorted(mapping):
        lines.append('  ["%s"] = "%s",' % (key, lua_escape(mapping[key])))
    lines.append("}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def gen_names():
    xy = load_pairs("/tmp/poke-corpus/corpus/XY/en_common.txt",
                    "/tmp/poke-corpus/corpus/XY/es_common.txt")
    moves, items = parse_tsv_names("/tmp/opencode/fr_names.tsv")

    def translate(name, overrides):
        if name in overrides:
            return overrides[name]
        es = xy.get(norm(name))
        if es:
            return es.upper()
        return name

    move_out, move_missing = {}, []
    for num, name in moves.items():
        if num == 0 or set(name) <= {"-"}:
            continue
        tr = translate(name, MOVE_OVERRIDES)
        move_out[g3_id_of(name)] = tr
        if tr == name and name not in MOVE_OVERRIDES and norm(name) not in xy:
            move_missing.append(name)

    item_out, item_missing = {}, []
    for num, name in items.items():
        if not name or set(name) <= {"?"}:
            continue
        tr = translate(name, ITEM_OVERRIDES)
        item_out[g3_id_of(name)] = tr
        if tr == name and name not in ITEM_OVERRIDES and norm(name) not in xy:
            item_missing.append(name)

    write_catalog(f"{MOD}/move_names.lua", move_out,
                  "-- translation-es-firered · nombres de movimientos (id = nombre EN)")
    write_catalog(f"{MOD}/item_names.lua", item_out,
                  "-- translation-es-firered · nombres de objetos (id = nombre EN)")
    print(f"Movimientos: {len(move_out)} (posibles gaps: {len(move_missing)} {move_missing})")
    print(f"Objetos    : {len(item_out)} (posibles gaps: {len(item_missing)} {item_missing})")


def gen_item_descriptions():
    with open("/tmp/opencode/fr_items.tsv", encoding="utf-8") as f:
        rows = [l.rstrip("\n").split("\t") for l in f if l.count("\t") >= 2]
    with open("/tmp/poke-corpus/corpus/FireRedLeafGreen/en_msg.txt",
              encoding="utf-8") as f:
        en = [l.rstrip("\n") for l in f]
    with open("/tmp/poke-corpus/corpus/FireRedLeafGreen/es_msg.txt",
              encoding="utf-8") as f:
        es = [l.rstrip("\n") for l in f]
    idx = {}
    for e, s in zip(en, es):
        if e and e not in idx:
            idx[e] = s

    out, missing = {}, []
    for row in rows:
        if len(row) < 3:
            continue
        name, desc = row[1], row[2]
        if not name or not desc or set(desc) <= {"?"}:
            continue
        tr = idx.get(desc)
        if tr:
            out[g3_id_of(name)] = tr
        else:
            missing.append((name, desc[:40]))

    write_catalog(f"{MOD}/item_descriptions.lua", out,
                  "-- translation-es-firered · descripciones de objetos (id = nombre EN)")
    print(f"Descripciones de objetos: {len(out)} (sin traducir: {len(missing)})")
    for n, d in missing[:15]:
        print(f"  [{n}] {d}")


if __name__ == "__main__":
    gen_names()
    gen_item_descriptions()
