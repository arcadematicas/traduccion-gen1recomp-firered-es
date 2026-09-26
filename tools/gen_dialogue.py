#!/usr/bin/env python3
"""Genera los catálogos de diálogo FireRed+LeafGreen (motor 0.3.x) como STRINGS
en el formato pret que acepta G3.textIr/TextIR.fromAscii.

Mapea los marcadores del corpus a la sintaxis del motor:
  [PLAYER] -> {PLAYER}   [RIVAL] -> {RIVAL}   [STR_VAR_n] -> {STR_VAR_n}
  [B_*]    -> {B_*}      (placeholders de batalla)
  [TAG]    -> {TAG}      (tags: PKMN, A_BUTTON, FONT_*, EMOJI_*, ...)
  \\n -> \\n   \\c -> \\p   \\r -> \\l
"""
import re

CORPUS = "/tmp/opencode/poke-corpus/corpus/FireRedLeafGreen"
OUTDIR = "/tmp/opencode/repo/lang"

# --- tokens que el motor reconoce (de text_ir.lua) ---
B_TXT = set("""B_BUFF1 B_BUFF2 B_COPY_VAR_1 B_COPY_VAR_2 B_COPY_VAR_3 B_PLAYER_MON1_NAME
B_OPPONENT_MON1_NAME B_PLAYER_MON2_NAME B_OPPONENT_MON2_NAME B_LINK_PLAYER_MON1_NAME
B_LINK_OPPONENT_MON1_NAME B_LINK_PLAYER_MON2_NAME B_LINK_OPPONENT_MON2_NAME
B_ATK_NAME_WITH_PREFIX_MON1 B_ATK_PARTNER_NAME B_ATK_NAME_WITH_PREFIX B_DEF_NAME_WITH_PREFIX
B_EFF_NAME_WITH_PREFIX B_ACTIVE_NAME_WITH_PREFIX B_SCR_ACTIVE_NAME_WITH_PREFIX B_CURRENT_MOVE
B_LAST_MOVE B_LAST_ITEM B_LAST_ABILITY B_ATK_ABILITY B_DEF_ABILITY B_SCR_ACTIVE_ABILITY
B_EFF_ABILITY B_TRAINER1_CLASS B_TRAINER1_NAME B_LINK_PLAYER_NAME B_LINK_PARTNER_NAME
B_LINK_OPPONENT1_NAME B_LINK_OPPONENT2_NAME B_LINK_SCR_TRAINER_NAME B_PLAYER_NAME
B_TRAINER1_LOSE_TEXT B_TRAINER1_WIN_TEXT B_26 B_PC_CREATOR_NAME B_ATK_PREFIX1 B_DEF_PREFIX1
B_ATK_PREFIX2 B_DEF_PREFIX2 B_ATK_PREFIX3 B_DEF_PREFIX3 B_TRAINER2_LOSE_TEXT B_TRAINER2_WIN_TEXT
B_BUFF3""".split())
KEYGFX = set("""A_BUTTON B_BUTTON L_BUTTON R_BUTTON START_BUTTON SELECT_BUTTON DPAD_UP DPAD_DOWN
DPAD_LEFT DPAD_RIGHT DPAD_UPDOWN DPAD_LEFTRIGHT DPAD_ANY""".split())
TAGS = {"PK", "MN", "PKMN", "PLUS", "LV_2", "PP", "ID", "LEFT_PAREN", "RIGHT_PAREN",
        "EMOJI_UNDERSCORE", "EMOJI_PIPE", "EMOJI_HIGHBAR", "EMOJI_TILDE", "EMOJI_LEFT_PAREN",
        "EMOJI_RIGHT_PAREN", "EMOJI_UNION", "EMOJI_GREATER_THAN", "EMOJI_LEFT_EYE",
        "EMOJI_RIGHT_EYE", "EMOJI_AT", "EMOJI_SEMICOLON", "EMOJI_PLUS", "EMOJI_MINUS",
        "EMOJI_EQUALS", "EMOJI_SPIRAL", "EMOJI_TONGUE", "EMOJI_TRIANGLE_OUTLINE", "EMOJI_ACUTE",
        "EMOJI_GRAVE", "EMOJI_CIRCLE", "EMOJI_TRIANGLE", "EMOJI_SQUARE", "EMOJI_HEART",
        "EMOJI_MOON", "EMOJI_NOTE", "EMOJI_BALL", "EMOJI_BOLT", "EMOJI_LEAF", "EMOJI_FIRE",
        "EMOJI_WATER", "EMOJI_LEFT_FIST", "EMOJI_RIGHT_FIST", "EMOJI_BIGWHEEL",
        "EMOJI_SMALLWHEEL", "EMOJI_SPHERE", "EMOJI_IRRITATED", "EMOJI_MISCHIEVOUS",
        "EMOJI_HAPPY", "EMOJI_ANGRY", "EMOJI_SURPRISED", "EMOJI_BIGSMILE", "EMOJI_EVIL",
        "EMOJI_TIRED", "EMOJI_NEUTRAL", "EMOJI_SHOCKED", "EMOJI_BIGANGER"}

def mappable(tok):
    if tok in ("PLAYER", "RIVAL", "STR_VAR_1", "STR_VAR_2", "STR_VAR_3"):
        return True
    if tok in B_TXT or tok in KEYGFX or tok in TAGS:
        return True
    if re.match(r"^(FONT_|COLOR|SHADOW|HIGHLIGHT|BG)", tok):
        return True
    return False

TOKEN_RE = re.compile(r"\[([A-Z_0-9]+)\]")

def convert(es):
    """Devuelve (string_pret, ok). ok=False si hay marcador no mapeable."""
    out = []
    i, n = 0, len(es)
    while i < n:
        ch = es[i]
        if ch == "\\" and i + 1 < n:
            nx = es[i+1]
            if nx == "n": out.append("\n"); i += 2; continue
            if nx in ("c", "p"): out.append("\\p"); i += 2; continue
            if nx in ("r", "l"): out.append("\\l"); i += 2; continue
            out.append(ch); i += 1; continue
        if ch == "[":
            j = es.find("]", i)
            if j == -1:
                out.append(ch); i += 1; continue
            tok = es[i+1:j]
            if not mappable(tok):
                return None, False
            out.append("{" + tok + "}")
            i = j + 1; continue
        out.append(ch); i += 1
    return "".join(out), True

def load_lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]

en = load_lines(CORPUS + "/en_msg.txt")
esv = load_lines(CORPUS + "/es_msg.txt")
en2es = {}
for e, s in zip(en, esv):
    if e and e not in en2es:
        en2es[e] = s

def read_tsv(p):
    d = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3: continue
            d[parts[0]] = (parts[1] == "1", parts[2])
    return d

fr = read_tsv("/tmp/opencode/fr_new2.tsv")
lg = read_tsv("/tmp/opencode/lg_new2.tsv")

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

def build(pairs):
    got, stats = {}, {"nomatch": 0, "unmappable": 0}
    for key, (cx, en_txt) in pairs.items():
        es = en2es.get(en_txt)
        if es is None:
            stats["nomatch"] += 1; continue
        conv, ok = convert(es)
        if not ok:
            stats["unmappable"] += 1; continue
        got[key] = conv
    return got, stats

common = {k: fr[k] for k in fr if k in lg and fr[k][1] == lg[k][1]}
fr_only = {k: v for k, v in fr.items() if k not in common}
lg_only = {k: v for k, v in lg.items() if k not in common}

def write(path, header, got):
    lines = [header, "return {"]
    for key in sorted(got):
        lines.append('  ["%s"] = "%s",' % (lua_escape(key), lua_escape(got[key])))
    lines.append("}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

c, cs = build(common)
f, fs = build(fr_only)
l, ls = build(lg_only)
write(OUTDIR + "/dialogue.lua", "-- translation-es-firered · diálogo común FireRed+LeafGreen", c)
write(OUTDIR + "/dialogue_firered.lua", "-- translation-es-firered · diálogo FireRed", f)
write(OUTDIR + "/dialogue_leafgreen.lua", "-- translation-es-firered · diálogo LeafGreen", l)

print(f"común     : {len(c):5d} | {cs}")
print(f"firered   : {len(f):5d} | {fs}")
print(f"leafgreen : {len(l):5d} | {ls}")
print(f"TOTAL     : {len(c)+len(f)+len(l)}")
