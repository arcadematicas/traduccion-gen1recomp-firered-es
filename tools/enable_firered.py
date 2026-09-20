#!/usr/bin/env python3
"""Activa el mod `translation-es-firered` en el options.lua de gen1recomp.

Uso:
    python3 enable_firered.py [ruta/a/options.lua]

Si no se indica ruta, usa la ubicación habitual en este equipo. Hace copia de
seguridad (.bak-firered) antes de escribir.

Nota: en gen1recomp 0.2.66/0.2.67 el estado de los mods vive en
`modsByVersion[version][modId]` (y `enabledByVersion` dentro del perfil). Para
FireRed hay que añadir un bucket `firered`. Alternativamente, si el lanzador de
mods ya permite activarlo a mano, este script no hace falta.
"""
import shutil
import sys

DEFAULT = ("/run/media/fransis/ROMS16TB/batocera/roms/linuxgames/gen1recomp/"
           "gen1recomp-x86_64.AppImage.home/.local/share/pokemon-love2d/options.lua")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    with open(path, encoding="utf-8") as f:
        c = f.read()
    shutil.copyfile(path, path + ".bak-firered")

    changed = 0

    # 1) enabledByVersion (indent 6)
    old1 = '      enabledByVersion = {\n'
    if 'firered = {\n          ["translation-es-firered"]' not in c:
        new1 = (old1 + '        firered = {\n'
                '          ["translation-es-firered"] = true,\n'
                '        },\n')
        assert c.count(old1) == 1, "enabledByVersion no encontrado"
        c = c.replace(old1, new1, 1)
        changed += 1

    # 2) modsByVersion (indent 4)
    old2 = '  modsByVersion = {\n'
    if 'firered = {\n      ["translation-es-firered"]' not in c:
        new2 = (old2 + '    firered = {\n'
                '      ["translation-es-firered"] = true,\n'
                '    },\n')
        assert c.count(old2) == 1, "modsByVersion no encontrado"
        c = c.replace(old2, new2, 1)
        changed += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("options.lua: %d cambios" % changed)


if __name__ == "__main__":
    main()
