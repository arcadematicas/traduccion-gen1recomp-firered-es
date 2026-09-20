#!/usr/bin/env python3
"""Genera lang/dialogue.lua para el mod translation-es-firered.

Convierte el corpus paralelo EN/ES de FireRed a la forma IR que espera el motor
gen1recomp 0.2.66 para el registro `text` en Gen 3.
"""
import re
import sys

CORPUS = "/tmp/poke-corpus/corpus/FireRedLeafGreen"
CLASS_TSV = "/tmp/opencode/fr_class.tsv"
OUT = "/tmp/opencode/repo/translation-es-firered/lang/dialogue.lua"


def load_lines(path):
    with open(path, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


def build_es_index():
    en = load_lines(f"{CORPUS}/en_msg.txt")
    es = load_lines(f"{CORPUS}/es_msg.txt")
    idx = {}
    for e, s in zip(en, es):
        if e and e not in idx:
            idx[e] = s
    return idx


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


MARKERS = {
    "[PLAYER]": ('player', None),
    "[RIVAL]": ('rival', None),
    "[STR_VAR_1]": ('strvar', 1),
    "[STR_VAR_2]": ('strvar', 2),
    "[STR_VAR_3]": ('strvar', 3),
}
KNOWN_EXTRA = {
    "[SUPER_ER]": "º",
    "[SUPER_E]": "º",
    "[SUPER_RE]": "º",
}


def parse_ir(es):
    """Devuelve (ir, error). ir es lista de comandos; error != None si hay un
    marcador desconocido."""
    ir = []
    buf = []

    def flush():
        if buf:
            ir.append({"t": "text", "s": "".join(buf)})
            buf.clear()

    i = 0
    n = len(es)
    while i < n:
        ch = es[i]
        if ch == "\\" and i + 1 < n:
            nxt = es[i + 1]
            if nxt == "n":
                flush(); ir.append({"t": "nl"}); i += 2; continue
            if nxt == "c":
                flush(); ir.append({"t": "para"}); i += 2; continue
            if nxt == "r":
                flush(); ir.append({"t": "scroll"}); i += 2; continue
            if nxt == "p":
                flush(); ir.append({"t": "para"}); i += 2; continue
            if nxt == "l":
                flush(); ir.append({"t": "scroll"}); i += 2; continue
            # escape desconocido: se deja literal
            buf.append(ch); i += 1; continue
        if ch == "[":
            j = es.find("]", i)
            if j == -1:
                buf.append(ch); i += 1; continue
            token = es[i:j + 1]
            if token in MARKERS:
                flush()
                kind, num = MARKERS[token]
                cmd = {"t": kind}
                if num is not None:
                    cmd["n"] = num
                ir.append(cmd)
                i = j + 1
                continue
            if token in KNOWN_EXTRA:
                buf.append(KNOWN_EXTRA[token])
                i = j + 1
                continue
            return None, token
        buf.append(ch)
        i += 1
    flush()
    ir.append({"t": "eos"})
    return ir, None


def ir_to_lua(ir, indent="    "):
    lines = ["{"]
    for cmd in ir:
        if cmd["t"] == "text":
            lines.append('%s  { t = "text", s = "%s" },' % (indent, lua_escape(cmd["s"])))
        elif cmd["t"] == "strvar":
            lines.append('%s  { t = "strvar", n = %d },' % (indent, cmd["n"]))
        else:
            lines.append('%s  { t = "%s" },' % (indent, cmd["t"]))
    lines.append(indent + "}")
    return "\n".join(lines)


def main():
    idx = build_es_index()
    rows = []
    with open(CLASS_TSV, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.count("\t") < 2:
                continue
            key, types, en = line.split("\t", 2)
            rows.append((key, types, en))

    translated = {}
    skipped_marker = []
    no_match = []
    for key, types, en in rows:
        es = idx.get(en)
        if es is None:
            no_match.append(key)
            continue
        ir, bad = parse_ir(es)
        if bad is not None:
            skipped_marker.append((key, bad, es))
            continue
        translated[key] = ir

    out = ["-- translation-es-firered · diálogo ROM (registro text, IR Gen3)",
           "-- Generado desde el corpus paralelo EN/ES de FireRed/LeafGreen.",
           "return {"]
    for key in sorted(translated):
        lua_key = lua_escape(key).replace('\\"', '\\"')
        out.append('  ["%s"] = %s,' % (lua_key, ir_to_lua(translated[key])))
    out.append("}")
    text = "\n".join(out) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)

    total = len(rows)
    print(f"Entradas en text.lua : {total}")
    print(f"Traducidas           : {len(translated)} ({100*len(translated)/total:.1f}%)")
    print(f"Sin match en corpus  : {len(no_match)}")
    print(f"Descartadas (marcador): {len(skipped_marker)}")
    for key, bad, es in skipped_marker[:20]:
        print(f"   {key}: {bad}  {es[:60]!r}")
    if no_match:
        print("\nSin match (primeras 20):", no_match[:20])


if __name__ == "__main__":
    main()
