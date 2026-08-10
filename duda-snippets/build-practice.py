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


# Sin minificar: con el CSS aparte sobra margen, y asi los archivos se pueden
# leer y editar a mano.
def mcss(s):
    return s.strip()


def mhtml(s):
    return s.strip()


def mjs(s):
    return s.strip()



HERO_DIGEST = """
/* Hero calcado del Appellate Digest, que en Duda se ve bien. Los valores
   salen de comparar su widget contra la version de Vercel: el overlay plano
   deja ver el video, el padding es mas generoso y el alto es 100svh. */
.{s} .emp-hero {{
  min-height:100svh !important;
  padding:80px 28px 72px !important;
  justify-content:center !important;
  border-bottom:none !important;
}}
.{s} .emp-hero-overlay {{
  background:rgba(20,48,52,0.75) !important;
}}
.{s} .emp-hero-overlay::before {{ content:none !important; }}
.{s} .emp-hero h1 {{ font-size:68px !important; letter-spacing:-1.5px !important; }}
.{s} .emp-hero-sub {{ font-size:18px !important; max-width:440px !important; margin-bottom:36px !important; }}
@media(max-width:768px) {{
  .{s} .emp-hero {{ padding:120px 20px 48px !important; justify-content:flex-start !important; }}
  .{s} .emp-hero h1 {{ font-size:13vw !important; letter-spacing:-1px !important; }}
}}
@media(min-width:769px) {{
  .{s} .emp-hero {{ padding:100px 96px 88px !important; }}
  .{s} .emp-hero h1 {{ font-size:96px !important; letter-spacing:-3px !important; }}
  .{s} .emp-hero-sub {{ font-size:16px !important; }}
}}
"""

page = sys.argv[1]
name = os.path.splitext(os.path.basename(page))[0]
w = bw.build(page, SCOPE)

if '--css' in sys.argv:
    css = mcss(re.search(r'<style>(.*?)</style>', w, re.S).group(1)).replace('#' + SCOPE, '.' + SCOPE)
    # Esta regla no esta acotada al scope: se aplicaria a todo el sitio. Va en
    # el widget de cada pagina, no en el head comun.
    css = css.replace('html, body { overflow-x:hidden; }\n', '')
    out = '<style>' + css + HERO_DIGEST.format(s=SCOPE) + '</style>'
    f = 'duda-snippets/practice-CSS-COMUN.html'
    open(f, 'w', encoding='utf-8').write(out)
    print(f'{f}  ({len(out)} car.)  -> head del sitio, UNA sola vez')

body = mhtml(re.search(r'<div id="[^"]+">\n(.*)\n</div>\n\n<script>', w, re.S).group(1))
js   = mjs(re.search(r'<script>(.*?)</script>\s*$', w, re.S).group(1))
out  = ('<style>html, body { overflow-x:hidden; }</style>\n\n'
        f'<div class="{SCOPE}">\n\n{body}\n\n</div>\n\n'
        f'<script>\n{js}\n</script>\n')
f = f'duda-snippets/{name}-MARKUP.html'
open(f, 'w', encoding='utf-8').write(out)
print(f'{f}  ({len(out)} car.)  -> widget de la pagina')

sch = bw.schema(page)
if sch:
    f = f'duda-snippets/{name}-SCHEMA.html'
    open(f, 'w', encoding='utf-8').write(sch + '\n')
    print(f'{f}  ({len(sch)} car.)  -> widget aparte, datos estructurados')
