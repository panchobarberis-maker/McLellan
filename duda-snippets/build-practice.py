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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enlaces as en

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

ENLACES = """
/* Breadcrumb y paginas relacionadas. Las subpaginas funcionan como landing
   pages, asi que necesitan links propios en el cuerpo: la nav de Duda no le
   dice a Google que estas 38 cuelgan de una practica en particular. */
/* Va entre el hero y el contenido, los dos verdes, asi que el breadcrumb
   toma el mismo verde: si no, queda una franja blanca cortando la pagina. */
.{s} .mlg-miga {{
  background:#1e3a3e !important; padding:26px 28px 0 !important;
}}
.{s} .mlg-miga-inner {{
  max-width:1100px !important; margin:0 auto !important;
  font-size:15px !important; color:#9fb0b2 !important; letter-spacing:0.2px !important;
}}
.{s} .mlg-miga a {{ color:#e8cc8a !important; text-decoration:none !important;
  border-bottom:1px solid rgba(201,169,110,0.5) !important; font-weight:600 !important; }}
.{s} .mlg-miga a:hover {{ color:#fff !important; border-bottom-color:#fff !important; }}
.{s} .mlg-miga span {{ margin:0 8px !important; color:#5f7476 !important; }}
@media(min-width:769px) {{
  .{s} .mlg-miga {{ padding:30px 80px 0 !important; }}
}}
@media(max-width:768px) {{
  .{s} .mlg-miga {{ padding:20px 20px 0 !important; }}
  .{s} .mlg-miga-inner {{ font-size:14px !important; }}
}}

.{s} .mlg-link-tema {{
  color:#1e3a3e !important; font-weight:700 !important; text-decoration:none !important;
  border-bottom:2px solid rgba(201,169,110,0.75) !important;
}}
.{s} .mlg-link-tema:hover {{ color:#b8933a !important; border-bottom-color:#b8933a !important; }}

.{s} .mlg-relacionadas {{
  background:#fbf6ef !important; padding:72px 28px !important; text-align:center !important;
}}
.{s} .mlg-relacionadas h2 {{
  font-family:'Barlow Condensed',sans-serif !important; font-weight:800 !important;
  text-transform:uppercase !important; font-size:38px !important;
  letter-spacing:-0.5px !important; color:#1e3a3e !important; margin:0 0 34px !important;
}}
.{s} .mlg-relacionadas-grid {{
  max-width:1100px !important; margin:0 auto !important; display:grid !important;
  grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)) !important; gap:16px !important;
}}
.{s} .mlg-relacionadas a {{
  display:block !important; background:#fff !important; border:1px solid #e6dcc9 !important;
  border-radius:12px !important; padding:24px 22px !important; text-align:left !important;
  color:#1e3a3e !important; text-decoration:none !important; font-size:19px !important;
  font-weight:700 !important; line-height:1.35 !important;
  box-shadow:0 2px 10px rgba(30,58,62,0.06);
  transition:transform 0.2s ease, box-shadow 0.2s ease;
}}
.{s} .mlg-relacionadas a:hover {{
  transform:translateY(-3px); box-shadow:0 10px 24px rgba(30,58,62,0.12);
  border-color:#c9a96e !important;
}}
.{s} .mlg-relacionadas a::after {{
  content:' \\2192'; color:#b8933a !important;
}}
@media(max-width:768px) {{
  .{s} .mlg-relacionadas {{ padding:52px 20px !important; }}
  .{s} .mlg-relacionadas h2 {{ font-size:30px !important; }}
  .{s} .mlg-relacionadas a {{ font-size:18px !important; padding:20px 18px !important; }}
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
    out = '<style>' + css + HERO_DIGEST.format(s=SCOPE) + ENLACES.format(s=SCOPE) + '</style>'
    f = 'duda-snippets/practice-CSS-COMUN.html'
    open(f, 'w', encoding='utf-8').write(out)
    print(f'{f}  ({len(out)} car.)  -> head del sitio, UNA sola vez')

    # El CSS comun sale de UNA pagina y lo usan las 38. Si alguna trae una regla
    # distinta, en Duda se veria mal y no habria forma de darse cuenta mirando,
    # asi que se compara aca y se avisa. Si esto no imprime nada, el bloque del
    # head sirve para las 38 y no hay que volver a tocarlo.
    def _reglas(texto):
        d = {}
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', texto):
            d.setdefault(' '.join(m.group(1).split()), set()).add(' '.join(m.group(2).split()))
        return d

    patron = _reglas(re.search(r'<style>(.*?)</style>', w, re.S).group(1))
    desvios = 0
    for otra in sorted(en.DE_QUIEN):
        if otra == name:
            continue
        suyas = _reglas(re.search(r'<style>(.*?)</style>',
                                  bw.build(otra + '.html', SCOPE), re.S).group(1))
        for sel, decl in suyas.items():
            if sel not in patron:
                print(f'  OJO  {otra}: regla que la comun no tiene -> {sel[:70]}')
                desvios += 1
            elif decl != patron[sel] and 'emp-hero' not in sel:
                print(f'  OJO  {otra}: {sel[:60]} difiere de la comun')
                desvios += 1
    print(f'  control: {desvios} desvios entre las 38 paginas')

body = mhtml(re.search(r'<div id="[^"]+">\n(.*)\n</div>\n\n<script>', w, re.S).group(1))


def con_enlaces(body, name):
    """Le da a la pagina los links internos que la nav de Duda no aporta."""
    madre = en.DE_QUIEN.get(name)
    if not madre:
        return body
    nombre_madre = en.MADRES[madre]

    # 1. Menciones reales a paginas hermanas, enlazadas dentro del texto.
    #    El nombre de la practica madre casi nunca aparece en los parrafos, pero
    #    los temas vecinos si: una pagina de wrongful termination habla de
    #    discriminacion y de represalias. Ese es el link que de verdad ayuda.
    #    Maximo tres, y una sola vez cada uno, para no llenar el texto de azul.
    #    Se recorre nodo de texto por nodo de texto, salteando titulos y lo que
    #    ya esta dentro de un link: buscar dentro del parrafo entero no alcanza,
    #    porque cualquier <strong> en el medio corta la frase en dos.
    partes = re.split(r'(<[^>]*>)', body)

    def salteable(i):
        prof_a = prof_h = 0
        for p in partes[:i]:
            if not p.startswith('<'):
                continue
            if re.match(r'<a\b', p):    prof_a += 1
            elif p.startswith('</a'):   prof_a -= 1
            elif re.match(r'<h[1-3]\b', p): prof_h += 1
            elif re.match(r'</h[1-3]', p):  prof_h -= 1
        return prof_a > 0 or prof_h > 0

    puestos = 0
    for v in en.GRUPOS[madre]:
        if v == name or puestos >= 3:
            continue
        eti = en.etiqueta(v)
        # El nombre completo primero; si no aparece, la version sin la palabra
        # generica del final, que es como lo suele nombrar el texto corrido.
        corto = re.sub(r'\s*\b(disputes|claims|matters|violations|rights)\b\s*$', '', eti,
                       flags=re.I).strip()
        for frase in [eti, corto] if corto != eti else [eti]:
            if len(frase) < 6:
                continue
            # El & del nombre puede venir escrito &amp; en el HTML. Se reemplaza
            # la version ya escapada, que es "\&", no el caracter suelto.
            crudo = re.escape(frase).replace(re.escape('&'), '(?:&|&amp;)')
            patron = re.compile(r'\b' + crudo + r'\b', re.IGNORECASE)
            puesto = False
            for i, p in enumerate(partes):
                if p.startswith('<') or salteable(i):
                    continue
                nuevo, cuantos = patron.subn(
                    lambda m: f'<a class="mlg-link-tema" href="/{v}">{m.group(0)}</a>', p, count=1)
                if cuantos:
                    partes[i] = nuevo
                    puesto = True
                    break
            if puesto:
                puestos += 1
                break
    body = ''.join(partes)

    # 2. Breadcrumb, arriba de todo el contenido, apenas termina el hero.
    miga = (f'<div class="mlg-miga"><div class="mlg-miga-inner">'
            f'<a href="/">Home</a><span>/</span>'
            f'<a href="{madre}">{nombre_madre}</a><span>/</span>{en.etiqueta(name)}'
            f'</div></div>\n')
    body = body.replace('<section class="content-section">',
                        miga + '<section class="content-section">', 1)

    # 3. Paginas relacionadas, justo antes del cierre con el formulario.
    vecinas = en.hermanas(name)
    if vecinas:
        tarjetas = '\n'.join(
            f'    <a href="/{v}">{en.etiqueta(v)}</a>' for v in vecinas)
        bloque = (f'<section class="mlg-relacionadas">\n'
                  f'  <h2 class="reveal">Related {nombre_madre} Matters</h2>\n'
                  f'  <div class="mlg-relacionadas-grid reveal reveal-d1">\n'
                  f'{tarjetas}\n  </div>\n</section>\n\n')
        body = body.replace('<section class="cta-banner"', bloque + '<section class="cta-banner"', 1)
    return body


body = con_enlaces(body, name)
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
