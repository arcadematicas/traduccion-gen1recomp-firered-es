#!/usr/bin/env python3
import re
ENGINE = "/tmp/opencode/engine320_strings.txt"
GSC = ("/run/media/fransis/ROMS16TB/batocera/roms/linuxgames/gen1recomp/"
       "gen1recomp-x86_64.AppImage.home/.local/share/pokemon-love2d/mods/"
       "translation-es-goldilvercrystal/lang/strings.lua")
OUT = "/tmp/opencode/repo/lang/strings.lua"

def lua_unescape(s):
    out=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c!='\\': out.append(c); i+=1; continue
        i+=1
        if i>=n: out.append('\\'); break
        e=s[i]
        simple={'n':'\n','t':'\t','r':'\r','a':'\a','b':'\b','f':'\f','v':'\v','\\':'\\','"':'"',"'":"'"}
        if e in simple: out.append(simple[e]); i+=1
        elif e=='x':
            m=re.match(r'[0-9a-fA-F]{2}', s[i+1:i+3])
            if m: out.append(chr(int(m.group(0),16))); i+=3
            else: out.append('x'); i+=1
        elif e.isdigit():
            m=re.match(r'\d{1,3}', s[i:])
            if m: out.append(chr(int(m.group(0),10))); i+=len(m.group(0))
        else: out.append(e); i+=1
    return ''.join(out)

def lua_escape(s):
    out=[]
    for ch in s:
        o=ord(ch)
        if ch=='"': out.append('\\"')
        elif ch=='\\': out.append('\\\\')
        elif ch=='\n': out.append('\\n')
        elif ch=='\t': out.append('\\t')
        elif o<32 or o==127: out.append('\\%03d'%o)
        else: out.append(ch)
    return ''.join(out)

gsc={}
with open(GSC,encoding='utf-8') as f: body=f.read()
for m in re.finditer(r'\["((?:[^"\\]|\\.)*)"\]\s*=\s*"((?:[^"\\]|\\.)*)"', body):
    k=lua_unescape(m.group(1)); v=lua_unescape(m.group(2))
    if k not in gsc: gsc[k]=v

found={}; missing=0
for line in open(ENGINE,encoding='utf-8'):
    lit=line.rstrip('\n')
    if not lit: continue
    s=lit.strip()
    if s[:1] in ('"',"'"): s=s[1:-1]
    s=lua_unescape(s)
    if not s.strip(): continue
    tr=gsc.get(s)
    if tr and tr.strip() and tr!=s: found[s]=tr
    else: missing+=1

lines=["-- translation-es-firered · textos propios del motor (registro strings)","return {"]
for k in sorted(found):
    lines.append('  ["%s"] = "%s",'%(lua_escape(k), lua_escape(found[k])))
lines.append("}")
open(OUT,"w",encoding="utf-8").write("\n".join(lines)+"\n")
print(f"strings motor: {sum(1 for _ in open(ENGINE,encoding='utf-8'))} | reutilizados: {len(found)} | sin traducción: {missing}")
