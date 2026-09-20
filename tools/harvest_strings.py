#!/usr/bin/env python3
"""Extrae del código fuente del motor todos los literales que pasan por
src/core/Strings.lua (registro `strings`), uno por línea.

Uso:
    python3 harvest_strings.py <ruta_al_src_del_motor> > engine_strings.txt

El motor no envía el fuente en la AppImage como .lua suelto: hay que extraerlo
del `.love` (que es un zip), p. ej.:

    mkdir engine && cd engine && unzip -q .../gen1recomp-0.2.XX.love
    python3 harvest_strings.py engine/src > engine_strings.txt
"""
import os
import re
import sys

# Mismo patrón que usa tools/modkit.py (harvest_engine_strings).
STRINGS_CALL = re.compile(
    r'\bStrings(?:\.source)?\('
    r'\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')\s*(?:,|\))')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    seen, out = set(), []
    for root, _dirs, names in os.walk(src):
        for name in sorted(names):
            if not name.endswith(".lua"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                body = f.read()
            for m in STRINGS_CALL.finditer(body):
                lit = m.group(1)
                if lit.startswith("'"):
                    lit = '"' + lit[1:-1].replace('"', '\\"') + '"'
                if lit not in seen:
                    seen.add(lit)
                    out.append(lit)
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
