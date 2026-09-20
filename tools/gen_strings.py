#!/usr/bin/env python3
"""Genera lang/strings.lua reutilizando las traducciones del mod GSC."""
import re

ENGINE_STRINGS = "/tmp/opencode/engine_strings.txt"
GSC_STRINGS = ("/run/media/fransis/ROMS16TB/batocera/roms/linuxgames/gen1recomp/"
               "gen1recomp-x86_64.AppImage.home/.local/share/pokemon-love2d/mods/"
               "translation-es-goldilvercrystal/lang/strings.lua")
OUT = "/tmp/opencode/repo/translation-es-firered/lang/strings.lua"


def lua_unescape(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out.append(c); i += 1; continue
        i += 1
        if i >= n:
            out.append("\\"); break
        e = s[i]
        simple = {"n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b",
                  "f": "\f", "v": "\v", "\\": "\\", '"': '"', "'": "'"}
        if e in simple:
            out.append(simple[e]); i += 1
        elif e == "x":
            m = re.match(r"[0-9a-fA-F]{2}", s[i + 1:i + 3])
            if m:
                out.append(chr(int(m.group(0), 16))); i += 3
            else:
                out.append("x"); i += 1
        elif e.isdigit():
            m = re.match(r"\d{1,3}", s[i:])
            if m:
                out.append(chr(int(m.group(0), 10))); i += len(m.group(0))
        else:
            out.append(e); i += 1
    return "".join(out)


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


def parse_catalog(path):
    with open(path, encoding="utf-8") as f:
        body = f.read()
    out = {}
    for m in re.finditer(r'\["((?:[^"\\]|\\.)*)"\]\s*=\s*"((?:[^"\\]|\\.)*)"', body):
        key = lua_unescape(m.group(1))
        val = lua_unescape(m.group(2))
        if key not in out:
            out[key] = val
    return out


def main():
    gsc = parse_catalog(GSC_STRINGS)
    print("Catálogo GSC:", len(gsc), "entradas")

    engine = []
    with open(ENGINE_STRINGS, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            engine.append(line)

    def literal_to_string(lit):
        lit = lit.strip()
        if lit[:1] in ('"', "'"):
            lit = lit[1:-1]
        return lua_unescape(lit)

    found, missing = {}, []
    for lit in engine:
        s = literal_to_string(lit)
        if not s.strip():
            continue
        tr = gsc.get(s)
        if tr and tr.strip() and tr != s:
            found[s] = tr
        else:
            missing.append(s)

    out = ["-- translation-es-firered · textos propios del motor (registro strings)",
           "-- Reutilizados del mod translation-es-goldilvercrystal (mismo motor).",
           "return {"]
    for key in sorted(found):
        out.append('  ["%s"] = "%s",' % (lua_escape(key), lua_escape(found[key])))
    out.append("}")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print(f"Strings del motor : {len(engine)}")
    print(f"Reutilizados      : {len(found)}")
    print(f"Sin traducción    : {len(missing)}")


if __name__ == "__main__":
    main()
