#!/usr/bin/env python3
"""Convierte una pagina del repo en un widget HTML para pegar en Duda.

    python3 duda-snippets/build-widget.py employment-law.html mlg-emp

Que hace:
  - saca doctype, <head>, <nav> y el menu mobile
  - acota todo el CSS a #<scope> para que no se mezcle con el tema de Duda
  - fuerza !important en las propiedades que el tema de Duda pisa
  - da full-bleed a las secciones, que Duda encajona dentro de un ROW
"""
import re, sys, os

# Duda pisa estas con !important desde su tema. Las de animacion quedan afuera
# a proposito: un !important sobre transform/opacity/box-shadow mata los
# @keyframes y los reveal por scroll.
FORCE = {
    'color', 'background', 'background-color', 'background-image', 'background-size',
    'font-family', 'font-size', 'font-weight', 'font-style', 'line-height',
    'letter-spacing', 'text-transform', 'text-align', 'text-decoration',
    'margin', 'margin-top', 'margin-bottom', 'margin-left', 'margin-right',
    'padding', 'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
    'border', 'border-top', 'border-bottom', 'border-left', 'border-right',
    'border-radius', 'border-color', 'border-width', 'border-style',
    'display', 'position', 'width', 'max-width', 'min-width',
    'height', 'max-height', 'min-height', 'list-style', 'gap',
}

NAV = ('.nav', '.logo-link', '.logo-img', '.dropdown', '.mobile-menu', '.mobile-accordion',
       '.nav-links', '.nav-hamburger', '.nav-logo-center', '.nav-contact-mobile', '.mobile-menu-close')

FONTS = ("https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800"
         "&family=Barlow+Condensed:wght@700;800;900&family=DM+Serif+Display:ital@0;1&display=swap")


# Rutas reales en Duda. Por defecto el slug es el nombre del archivo; aca van
# las que no coinciden. Si Duda usa otro slug, se cambia solo esta tabla y se
# regeneran todas las paginas de una.
SLUGS = {
    'index':               '/',
    'business-litigation': '/civil-litigation',
    'contact':             '/contact-us',
}


def to_duda(href):
    """wrongful-termination.html -> /wrongful-termination"""
    name = href[:-5]
    return SLUGS.get(name, '/' + name)


def is_nav(sel):
    s = sel.strip()
    return any(s == n or s.startswith(n + c) for n in NAV for c in (' ', ':', '.', ',', '>'))


def force_important(decls):
    out = []
    for d in decls.split(';'):
        if ':' not in d:
            out.append(d); continue
        prop = d.split(':', 1)[0].strip().lower()
        if prop in FORCE and '!important' not in d:
            d = d.rstrip() + ' !important'
        out.append(d)
    return ';'.join(out)


def scope_block(text, scope):
    out, i, n = [], 0, len(text)
    while i < n:
        at = text.find('{', i)
        if at == -1:
            break
        head = text[i:at]
        depth, j = 1, at + 1
        while j < n and depth:
            if text[j] == '{': depth += 1
            elif text[j] == '}': depth -= 1
            j += 1
        inner, h = text[at + 1:j - 1], head.strip()

        if h.startswith(('@keyframes', '@-webkit-keyframes', '@font-face')):
            out.append('\n' + h + ' {' + inner + '}')          # sin tocar
        elif h.startswith(('@media', '@supports')):
            out.append('\n' + h + ' {' + scope_block(inner, scope) + '\n}')
        else:
            keep = [s for s in h.split(',') if s.strip() and not is_nav(s)]
            if keep:
                sels = []
                for s in keep:
                    s = s.strip()
                    if s in ('html', 'body') or s.startswith('html '):
                        sels.append('#' + scope)
                    elif s.startswith('*'):
                        sels.append('#' + scope + ' ' + (s if s != '*' else '*'))
                    else:
                        sels.append('#' + scope + ' ' + s)
                out.append('\n' + ', '.join(sels) + ' {' + force_important(inner) + '}')
        i = j
    return ''.join(out)


def build(path, scope):
    src = open(path, encoding='utf-8').read()

    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)

    body = re.search(r'<body>(.*)</body>', src, re.S).group(1)
    body = re.sub(r'<nav\b.*?</nav>', '', body, flags=re.S)
    body = re.sub(r'<div class="mobile-menu".*?\n</div>\n', '', body, flags=re.S)

    # Los estilos inline tienen que llevar !important tambien: sin eso, el
    # !important que le ponemos a las reglas generales les gana y les pisa el
    # color (asi salieron blancas las respuestas de las FAQ de employees).
    def inline(m):
        return 'style="' + force_important(m.group(1)) + '"'
    body = re.sub(r'style="([^"]*)"', inline, body)

    # Links internos con la URL definitiva de Duda, para no tener que tocarlos
    # despues de publicar.
    body = re.sub(r'href="([a-z0-9-]+\.html)"',
                  lambda m: 'href="' + to_duda(m.group(1)) + '"', body)

    scripts = re.findall(r'<script>(.*?)</script>', body, re.S)
    body = re.sub(r'<script>.*?</script>', '', body, flags=re.S).strip()

    widget = f"""<style>
@import url('{FONTS}');
html, body {{ overflow-x:hidden; }}
#{scope} {{ font-family:'Barlow',sans-serif !important; color:#1e3a3e !important;
  -webkit-font-smoothing:antialiased; font-weight:500; }}

{scope_block(css, scope)}

/* Misma receta que el widget del Appellate Digest, que en Duda funciona bien:
   secciones a 100vw exacto; el hero desborda 2vw por lado solo en desktop y
   tapa con sombras arriba y abajo; en mobile vuelve a 100vw para no empujar
   los botones fuera de pantalla. */
#{scope} > section, #{scope} > div {{
  margin-left:calc(-50vw + 50%) !important;
  width:100vw !important; max-width:100vw !important;
}}
#{scope} > *:first-child {{
  margin-top:-8px !important;
  box-shadow:0 20px 0 0 #1e3a3e, 0 -60px 0 0 #1e3a3e !important;
  margin-left:calc(-52vw + 50%) !important;
  width:104vw !important; max-width:104vw !important;
}}
@media(max-width:768px) {{
  #{scope} > *:first-child {{
    margin-left:calc(-50vw + 50%) !important;
    width:100vw !important; max-width:100vw !important;
  }}
}}
</style>

<div id="{scope}">
{body}
</div>

<script>
{chr(10).join(scripts)}
</script>
"""
    return widget


def schema(path):
    """El JSON-LD vive en el <head> del original y el widget no se lo lleva.
    Duda no genera FAQPage por su cuenta, asi que hay que pegarlo aparte."""
    src = open(path, encoding='utf-8').read()
    head = src[:src.index('</head>')]
    return '\n'.join(re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S))


if __name__ == '__main__':
    page  = sys.argv[1]
    scope = sys.argv[2] if len(sys.argv) > 2 else 'mlg-' + os.path.splitext(os.path.basename(page))[0]
    out   = 'duda-snippets/' + os.path.splitext(os.path.basename(page))[0] + '-widget.html'
    w = build(page, scope)
    open(out, 'w', encoding='utf-8').write(w)
    print(f'{out}  ({round(len(w)/1024)} KB, scope #{scope})')

    sch = schema(page)
    if sch:
        f = out.replace('-widget.html', '-SCHEMA.html')
        open(f, 'w', encoding='utf-8').write(sch + '\n')
        print(f'{f}  ({len(sch)} car.)  -> widget aparte o panel de SEO')
