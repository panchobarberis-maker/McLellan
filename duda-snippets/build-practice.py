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
/* Hero calcado del Appellate Digest. Los tamanos dependen del ancho Y del
   alto de la ventana: en pantallas bajas todo se achica para que el hero
   entre completo en la primera vista sin tener que scrollear. */
.{s} .emp-hero {{
  min-height:calc(100svh - 62px) !important;   /* lo ajusta el script */
  padding:min(80px, 7vh) 28px min(72px, 6vh) !important;
  justify-content:center !important;
  border-bottom:none !important;
}}
.{s} .emp-hero-overlay {{
  background:rgba(20,48,52,0.75) !important;
}}
.{s} .emp-hero-overlay::before {{ content:none !important; }}
.{s} .emp-hero h1 {{
  font-size:min(68px, 11vh, 9vw) !important; letter-spacing:-1.5px !important;
  margin-bottom:min(18px, 2vh) !important;
}}
.{s} .hero-pill {{ margin-bottom:min(24px, 2.5vh) !important; }}
.{s} .emp-hero-sub {{
  font-size:min(18px, 2.4vh) !important; max-width:440px !important;
  margin-bottom:min(36px, 4vh) !important;
}}
@media(max-width:768px) {{
  .{s} .emp-hero {{ padding:min(120px, 12vh) 20px min(48px, 5vh) !important; justify-content:flex-start !important; }}
  .{s} .emp-hero h1 {{ font-size:min(13vw, 10vh) !important; letter-spacing:-1px !important; }}
}}
@media(min-width:769px) {{
  .{s} .emp-hero {{ padding:min(64px, 6vh) 96px min(56px, 5vh) !important; }}
  .{s} .emp-hero h1 {{ font-size:min(88px, 10.5vh, 6.4vw) !important; letter-spacing:-3px !important;
                       margin-bottom:min(14px, 1.6vh) !important; }}
  .{s} .emp-hero-sub {{ font-size:min(19px, 2.3vh) !important; margin-bottom:min(28px, 3vh) !important; }}
  .{s} .hero-pill {{ margin-bottom:min(18px, 2vh) !important; }}
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
FIT_HERO = '''
// El hero tiene que entrar en la primera vista. Arriba suyo esta el header de
// Duda, que mide distinto en desktop y en mobile, asi que en vez de un numero
// fijo medimos cuanto hay por encima y lo descontamos.
(function(){
  var hero = document.querySelector('.%s .emp-hero');
  if (!hero) return;
  function fit(){
    hero.style.minHeight = '';
    var arriba = hero.getBoundingClientRect().top + window.scrollY;
    hero.style.minHeight = 'calc(100svh - ' + Math.max(0, Math.round(arriba)) + 'px)';
  }
  fit();
  window.addEventListener('load', fit);
  window.addEventListener('resize', fit);
})();
''' % SCOPE

SAFE_REVEAL = '''
// Red de seguridad: si el observador no llega a disparar, nada queda invisible.
setTimeout(function(){
  document.querySelectorAll('.%s .reveal:not(.in-view)').forEach(function(el){
    if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in-view');
  });
}, 1200);
''' % SCOPE

BARRA = ''
if '--progreso' in sys.argv:
    BARRA = '''
// Barra de progreso: mide cuanto del contenido queda por leer.
(function(){
  var barra = document.querySelector('.%s-progress');
  var cont  = document.querySelector('.%s');
  if (!barra || !cont) return;
  function pintar(){
    var arriba = cont.getBoundingClientRect().top + window.scrollY;
    var recorrido = cont.offsetHeight - window.innerHeight;
    if (recorrido <= 0) { barra.style.width = '0'; return; }
    var hecho = (window.scrollY - arriba) / recorrido;
    barra.style.width = Math.max(0, Math.min(1, hecho)) * 100 + '%%';
  }
  pintar();
  window.addEventListener('scroll', pintar, {passive:true});
  window.addEventListener('resize', pintar);
})();
''' % (SCOPE, SCOPE)

ELEMENTO = f'<div class="{SCOPE}-progress"></div>\n' if '--progreso' in sys.argv else ''

out  = ('<style>html, body { overflow-x:hidden; }</style>\n\n' + ELEMENTO + '\n'
        f'<div class="{SCOPE}">\n\n{body}\n\n</div>\n\n'
        f'<script>\n{js}\n{FIT_HERO}{SAFE_REVEAL}{BARRA}</script>\n')
f = f'duda-snippets/{name}-MARKUP.html'
open(f, 'w', encoding='utf-8').write(out)
print(f'{f}  ({len(out)} car.)  -> widget de la pagina')

sch = bw.schema(page)
if sch:
    f = f'duda-snippets/{name}-SCHEMA.html'
    open(f, 'w', encoding='utf-8').write(sch + '\n')
    print(f'{f}  ({len(sch)} car.)  -> widget aparte, datos estructurados')
