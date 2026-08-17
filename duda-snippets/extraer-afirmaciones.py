#!/usr/bin/env python3
"""Saca de las paginas cada afirmacion que se pueda verificar.

    python3 duda-snippets/extraer-afirmaciones.py

Reemplaza al extractor anterior, que cortaba el texto en cada punto. Ese corte
partia los decimales: "1.5x" quedaba como "5x" y "seccion 1102.5" como
"seccion 1102". Las cuatro frases que se detectaron eran las visibles; el
problema es que cualquier oracion con un decimal pudo haberse verificado
contra un texto truncado.

Aca las oraciones se cortan solo donde termina una oracion de verdad: un punto
seguido de espacio y mayuscula, y nunca dentro de un numero, de una sigla ni
de una abreviatura conocida.
"""
import re, sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enlaces as en

# Abreviaturas que llevan punto y no terminan la oracion.
ABREV = {'e.g', 'i.e', 'vs', 'etc', 'no', 'inc', 'corp', 'ltd', 'mr', 'mrs', 'ms',
         'dr', 'jr', 'sr', 'st', 'ave', 'approx', 'u.s', 'cal', 'cal.app', 'art',
         'sec', 'subd', 'para', 'ch', 'pt', 'ed', 'rev', 'dept', 'div', 'reg', 'regs',
         'f.supp', 'f.2d', 'f.3d', 'cal.rptr'}

CORTE = re.compile(r'([.!?])(["\')\]]?)\s+(?=[A-Z(])')


def oraciones(texto):
    """Corta solo donde termina una oracion de verdad.

    Nunca despues de un digito, que es lo que partia 1.5x y la seccion 1102.5,
    y nunca despues de una abreviatura conocida. El look-behind de una regex no
    sirve para esto porque exige ancho fijo, asi que se revisa a mano lo que
    hay antes de cada candidato.
    """
    partes, ultimo = [], 0
    for m in CORTE.finditer(texto):
        antes = texto[:m.start()]
        if antes and antes[-1].isdigit():
            continue                                    # decimal, no es fin
        palabra = re.search(r'([A-Za-z.]+)$', antes)
        if palabra and palabra.group(1).lower().rstrip('.') in ABREV:
            continue                                    # abreviatura
        partes.append(texto[ultimo:m.end(2)].strip())
        ultimo = m.end()
    resto = texto[ultimo:].strip()
    if resto:
        partes.append(resto)
    return [p for p in partes if p]


def visible(ruta):
    t = open(ruta, encoding='utf-8').read()
    cuerpo = t[t.find('<body>'):]
    # Fuera del analisis: navegacion, migas, relacionadas y scripts, que no son
    # afirmaciones de la firma sino andamiaje.
    for patron in (r'<nav\b.*?</nav>', r'<script\b.*?</script>', r'<style\b.*?</style>',
                   r'<div class="mlg-miga".*?</div></div>',
                   r'<section class="mlg-relacionadas".*?</section>',
                   r'<div class="mobile-menu".*?\n</div>\n'):
        cuerpo = re.sub(patron, ' ', cuerpo, flags=re.S)
    texto = re.sub(r'<[^>]+>', ' ', cuerpo)
    texto = (texto.replace('&amp;', '&').replace('&quot;', '"')
                  .replace('&#39;', "'").replace('&nbsp;', ' ').replace('&sect;', '§'))
    return ' '.join(texto.split())


# Lo que hace verificable a una oracion: un plazo, un umbral, un monto, un
# porcentaje, una norma o un fallo.
VERIFICABLE = re.compile(
    r'\b\d+(?:\.\d+)?\s*(?:year|month|week|day|hour)s?\b'
    r'|\b\d+\s*or\s+more\s+employees\b'
    r'|\b\d+(?:\.\d+)?\s*(?:percent|%)'
    r'|\$\s?\d'
    r'|\b[Ss]ections?\s+\d+(?:\.\d+)?'
    r'|§+\s?\d+(?:\.\d+)?'
    r'|\b(?:AB|SB)\s?\d{1,4}\b'
    r'|\b[A-Z][A-Za-z\'-]+\s+v\.\s+[A-Z]'
    r'|\b\d+\s+Cal\.\s?(?:App\.\s?)?\d?(?:th|d)\b'
    r'|\b\d+\s+U\.S\.\s+\d+',
    re.X)


def main():
    paginas = ['employment-law'] + sorted(en.DE_QUIEN)
    filas, por_pagina = [], {}
    for p in paginas:
        ruta = p + '.html'
        if not os.path.exists(ruta):
            continue
        vistas = set()
        for o in oraciones(visible(ruta)):
            if len(o) < 40 or not VERIFICABLE.search(o) or o in vistas:
                continue
            vistas.add(o)
            filas.append((p, o))
            por_pagina.setdefault(p, []).append(o)
    return paginas, filas, por_pagina


if __name__ == '__main__':
    paginas, filas, por_pagina = main()
    json.dump([{'pagina': p, 'texto': o} for p, o in filas],
              open('duda-snippets/afirmaciones.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'{len(filas)} afirmaciones en {len(por_pagina)} paginas')
    for p in paginas:
        if p in por_pagina:
            print(f'  {len(por_pagina[p]):3}  {p}')
