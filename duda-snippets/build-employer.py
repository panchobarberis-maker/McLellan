#!/usr/bin/env python3
"""Prepara las paginas de employer (for employers) para Duda.

    python3 duda-snippets/build-employer.py wage-hour-defense.html

A diferencia de build-practice.py, esta NO llama a con_enlaces() de
enlaces.py: el breadcrumb via JSON-LD, el bloque "Related" y el schema
(BreadcrumbList + Service) ya estan escritos a mano en cada pagina, con
los pares exactos que pidio Claire (algunos cruzan a la pagina de
employee correspondiente, otros no, y no son una rotacion pareja). Si
se llamara a con_enlaces() aca, agregaria un segundo bloque "Related X
Matters" generico por rotacion y un segundo BreadcrumbList + Service,
duplicando lo que ya esta en la fuente.

bw.schema() sin pasarle madre simplemente devuelve los <script
type="application/ld+json"> que ya estan en el <head> de la pagina
(menos LegalService), asi que el FAQPage + BreadcrumbList + Service que
ya escribimos a mano viajan tal cual, sin que el pipeline los toque.
"""
import re, sys, os
import importlib.util

_spec = importlib.util.spec_from_file_location(
    'bw', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-widget.py'))
bw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bw)

page = sys.argv[1]
name = os.path.splitext(os.path.basename(page))[0]
scope = 'mlgE-' + name

w = bw.build(page, scope)
body = re.search(r'<div id="[^"]+">\n(.*)\n</div>\n\n<script>', w, re.S).group(1).strip()
css = re.search(r'<style>(.*)</style>', w, re.S).group(1)
js = re.search(r'<script>(.*)</script>\s*$', w, re.S).group(1).strip()

SAFE_REVEAL = f'''
// Red de seguridad: si el observador no llega a disparar, nada queda invisible.
setTimeout(function(){{
  document.querySelectorAll('#{scope} .reveal:not(.in-view)').forEach(function(el){{
    if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in-view');
  }});
}}, 1200);
'''

out = (f'<style>\n{css}\n</style>\n\n'
       f'<div id="{scope}">\n\n{body}\n\n</div>\n\n'
       f'<script>\n{js}\n{SAFE_REVEAL}</script>\n')

sch = bw.schema(page)
if sch:
    out += ('\n<!-- Datos estructurados de esta pagina. Ya van incluidos aca:\n'
            '     no hace falta un widget aparte. Si la pagina ya tiene uno con\n'
            '     este mismo JSON, borralo, o Google va a leer el FAQ dos veces. -->\n'
            + sch + '\n')

f = f'duda-snippets/{name}-MARKUP.html'
open(f, 'w', encoding='utf-8').write(out)
print(f'{f}  ({len(out)} car.)  -> widget de la pagina, schema incluido')

if sch:
    f = f'duda-snippets/{name}-SCHEMA.html'
    open(f, 'w', encoding='utf-8').write(sch + '\n')
    print(f'{f}  ({len(sch)} car.)  -> copia suelta, no hace falta pegarla')
