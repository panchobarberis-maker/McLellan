#!/usr/bin/env python3
"""Parte un widget de Duda en piezas que entren en el limite de caracteres.

    python3 duda-snippets/split-widget.py duda-snippets/employment-law-widget.html 45000

El widget HTML de Duda no guarda por encima de ~50.000 caracteres. En vez de
repetir el CSS en cada pieza, lo saca a un archivo aparte que va una sola vez
en Settings > Head HTML del sitio, y deja los widgets con puro markup.

El scope pasa de #id a .clase: cada pieza es un DOM separado, asi que todas
llevan el mismo <div class="...">. La especificidad no importa porque el CSS
ya viene con !important en lo que Duda pisa.
"""
import re, sys, os

path  = sys.argv[1]
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 45000

w = open(path, encoding='utf-8').read()
base = os.path.splitext(path)[0].replace('-widget', '')

style  = re.search(r'<style>(.*?)</style>', w, re.S).group(1)
scope  = re.search(r'<div id="([^"]+)">', w).group(1)
body   = re.search(r'<div id="[^"]+">\n(.*)\n</div>\n\n<script>', w, re.S).group(1)
script = re.search(r'<script>(.*?)</script>\s*$', w, re.S).group(1)

# de #scope a .scope, para que valga en las tres piezas
style = style.replace('#' + scope, '.' + scope)

# cortar el cuerpo por secciones de primer nivel
chunks, depth, start = [], 0, 0
for m in re.finditer(r'<(/?)(section|div)\b[^>]*?(/?)>', body):
    if m.group(3) == '/':
        continue
    depth += -1 if m.group(1) else 1
    if depth == 0:
        chunks.append(body[start:m.end()])
        start = m.end()
if start < len(body):
    chunks.append(body[start:])

# agrupar en piezas que entren en el limite
parts, cur = [], ''
for c in chunks:
    if cur and len(cur) + len(c) > LIMIT:
        parts.append(cur); cur = c
    else:
        cur += c
if cur:
    parts.append(cur)

head = f"""<style>
{style}</style>
"""
open(base + '-HEAD.html', 'w', encoding='utf-8').write(head)
print(f'{base}-HEAD.html  ({len(head)} car.)  -> Settings > Head HTML del sitio')

for i, p in enumerate(parts, 1):
    js = f'\n\n<script>\n{script}</script>\n' if i == len(parts) else ''
    out = f'<div class="{scope}">\n{p.strip()}\n</div>{js}'
    f = f'{base}-PARTE{i}.html'
    open(f, 'w', encoding='utf-8').write(out)
    flag = '  <-- OJO, pasa el limite' if len(out) > 50000 else ''
    print(f'{f}  ({len(out)} car.){flag}')
