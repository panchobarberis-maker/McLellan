#!/usr/bin/env python3
"""Prepara las practice pages para Duda con CSS compartido.

    python3 duda-snippets/build-practice.py wrongful-termination.html --css
    python3 duda-snippets/build-practice.py adverse-possession.html

Las 38 subpaginas usan el mismo diseno, asi que el CSS va UNA sola vez en el
head del sitio y cada pagina aporta solo su markup. Con --css tambien emite el
stylesheet comun (se hace una vez, desde cualquier pagina).
"""
import re, sys, os
import importlib.util

_spec = importlib.util.spec_from_file_location(
    'bw', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-widget.py'))
bw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bw)

SCOPE = 'mlgP'          # comun a todas las practice pages


def mcss(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'\s*\n\s*', ' ', s)
    s = re.sub(r'  +', ' ', s)
    s = re.sub(r'\s*([{};,])\s*', r'\1', s)
    s = re.sub(r':\s+', ':', s)
    return re.sub(r';}', '}', s).strip()      # no tocar espacios de calc()


def mhtml(s):
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'>\s+<', '><', s)
    return re.sub(r'\s{2,}', ' ', s).strip()


def mjs(s):
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'\s*\n\s*', '', s)
    return re.sub(r'\s{2,}', ' ', s).strip()


page = sys.argv[1]
name = os.path.splitext(os.path.basename(page))[0]
w = bw.build(page, SCOPE)

if '--css' in sys.argv:
    css = mcss(re.search(r'<style>(.*?)</style>', w, re.S).group(1)).replace('#' + SCOPE, '.' + SCOPE)
    out = f'<style>{css}</style>'
    f = 'duda-snippets/practice-CSS-COMUN.html'
    open(f, 'w', encoding='utf-8').write(out)
    print(f'{f}  ({len(out)} car.)  -> head del sitio, UNA sola vez')

body = mhtml(re.search(r'<div id="[^"]+">\n(.*)\n</div>\n\n<script>', w, re.S).group(1))
js   = mjs(re.search(r'<script>(.*?)</script>\s*$', w, re.S).group(1))
out  = f'<div class="{SCOPE}">{body}</div><script>{js}</script>'
f = f'duda-snippets/{name}-MARKUP.html'
open(f, 'w', encoding='utf-8').write(out)
print(f'{f}  ({len(out)} car.)  -> widget de la pagina')

sch = bw.schema(page)
if sch:
    f = f'duda-snippets/{name}-SCHEMA.html'
    open(f, 'w', encoding='utf-8').write(sch + '\n')
    print(f'{f}  ({len(sch)} car.)  -> widget aparte, datos estructurados')
