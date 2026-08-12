#!/usr/bin/env python3
"""Dice que widgets cambiaron desde la ultima vez que se pegaron en Duda.

    python3 duda-snippets/cambios.py            que hay que volver a pegar
    python3 duda-snippets/cambios.py --pegado   marca todo como ya pegado

El contenido vive dentro de un widget HTML, asi que Duda no deja editar una
palabra desde el editor: cualquier cambio de texto obliga a regenerar y pegar
de nuevo. Lo unico que se puede hacer es pegar lo minimo, y para eso hay que
saber exactamente que cambio. Sin esto la salida es repisar las 38 por las
dudas, que es media hora cada vez.

Guarda una huella de cada archivo en .duda-pegado.json. La huella ignora los
comentarios, asi que reescribir un comentario no cuenta como cambio.
"""
import hashlib, json, os, re, sys, glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, 'duda-snippets', '.duda-pegado.json')

# Lo que se pega en Duda, con el nombre que ve el usuario.
GRUPOS = [
    ('Site Head',      ['duda-snippets/SITE-HEAD.html']),
    ('Footer',         ['duda-snippets/FOOTER-2-LEGALES.html']),
    ('Widget',         sorted(glob.glob(os.path.join(RAIZ, 'duda-snippets/*-MARKUP.html')))),
    ('Schema',         sorted(glob.glob(os.path.join(RAIZ, 'duda-snippets/*-SCHEMA.html')))),
]


def huella(ruta):
    try:
        t = open(ruta, encoding='utf-8').read()
    except FileNotFoundError:
        return None
    # Los comentarios no cambian lo que se ve ni lo que lee Google.
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'^\s*//.*$', '', t, flags=re.M)
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    return hashlib.sha256(' '.join(t.split()).encode()).hexdigest()[:16]


def rel(p):
    return os.path.relpath(p if os.path.isabs(p) else os.path.join(RAIZ, p), RAIZ)


def actual():
    d = {}
    for _, archivos in GRUPOS:
        for a in archivos:
            h = huella(a if os.path.isabs(a) else os.path.join(RAIZ, a))
            if h:
                d[rel(a)] = h
    return d


def guardado():
    if not os.path.exists(REGISTRO):
        return {}
    return json.load(open(REGISTRO, encoding='utf-8'))


if __name__ == '__main__':
    hoy, antes = actual(), guardado()

    if '--pegado' in sys.argv:
        json.dump(hoy, open(REGISTRO, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        print(f'Registradas {len(hoy)} piezas como ya pegadas en Duda.')
        sys.exit()

    if not antes:
        print('No hay registro previo. Corre con --pegado despues de pegar todo\n'
              'en Duda, y a partir de ahi te digo solo lo que cambie.')
        sys.exit()

    nuevas = [f for f in hoy if f not in antes]
    distintas = [f for f in hoy if f in antes and hoy[f] != antes[f]]

    if not nuevas and not distintas:
        print('Nada que pegar: Duda esta al dia.')
        sys.exit()

    for etiqueta, archivos in GRUPOS:
        mios = [f for f in distintas if any(rel(a) == f for a in archivos)]
        nuevos = [f for f in nuevas if any(rel(a) == f for a in archivos)]
        for f in sorted(mios):
            print(f'  CAMBIO  {etiqueta:9} {os.path.basename(f)}')
        for f in sorted(nuevos):
            print(f'  NUEVO   {etiqueta:9} {os.path.basename(f)}')
    print(f'\n{len(distintas) + len(nuevas)} piezas para pegar, de {len(hoy)}.')
