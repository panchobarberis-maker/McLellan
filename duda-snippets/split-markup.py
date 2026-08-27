#!/usr/bin/env python3
"""Parte un *-MARKUP.html (salida de build-practice.py o build-employer.py)
en piezas que entren en el limite de ~50.000 caracteres de un widget de Duda.

    python3 duda-snippets/split-markup.py duda-snippets/faqs-MARKUP.html

A diferencia de split-widget.py (pensado para la salida cruda de
build-widget.py, con el CSS adentro), estos MARKUP.html ya tienen el CSS
compartido afuera (practice-CSS-COMUN.html / SITE-HEAD.html), asi que solo
hay que partir el <div class="mlgP">...</div> por secciones de primer nivel
y dejar el <script> final (el que revela el contenido al scrollear) y el
schema en la ULTIMA pieza, para que exista una sola vez en la pagina.
"""
import re, sys, os

LIMIT = 45000
path = sys.argv[1]
if len(sys.argv) > 2:
    LIMIT = int(sys.argv[2])

w = open(path, encoding='utf-8').read()
base = path[:-len('-MARKUP.html')] if path.endswith('-MARKUP.html') else os.path.splitext(path)[0]

m = re.search(r'<div class="([^"]+)">\n(.*)\n</div>\n\n<script>(.*?)</script>\n(.*)$', w, re.S)
if not m:
    sys.exit('No pude encontrar el div.mlgP / <script> final. Revisa el formato del archivo.')
scope, body, script, tail = m.group(1), m.group(2), m.group(3), m.group(4)

chunks, depth, start = [], 0, 0
for mm in re.finditer(r'<(/?)(section|div)\b[^>]*?(/?)>', body):
    if mm.group(3) == '/':
        continue
    depth += -1 if mm.group(1) else 1
    if depth == 0:
        chunks.append(body[start:mm.end()])
        start = mm.end()
if start < len(body):
    chunks.append(body[start:])

parts, cur = [], ''
for c in chunks:
    if cur and len(cur) + len(c) > LIMIT:
        parts.append(cur); cur = c
    else:
        cur += c
if cur:
    parts.append(cur)

for i, p in enumerate(parts, 1):
    extra = f'\n\n<script>{script}</script>\n{tail}' if i == len(parts) else ''
    out = f'<div class="{scope}">\n{p.strip()}\n</div>{extra}'
    f = f'{base}-PARTE{i}.html'
    open(f, 'w', encoding='utf-8').write(out)
    flag = '  <-- OJO, pasa el limite' if len(out) > 50000 else ''
    print(f'{f}  ({len(out)} car.){flag}')

print(f'\n{len(parts)} piezas. Pegar cada una en un widget de codigo distinto, en orden, todas en la misma zona de la pagina donde iba el widget original.')
