"""A que area pertenece cada subpagina y como se llama en pantalla.

Los grupos salen de los links que cada pagina madre ya tiene en su cuerpo, asi
que esto no inventa una jerarquia nueva: la copia de la que ya existe.

Sirve para dos cosas en el widget: el breadcrumb de arriba y el bloque de
paginas relacionadas de abajo.
"""
import re, os

# slug de la madre -> como se la nombra en el breadcrumb
MADRES = {
    '/employment-law':        'Employment Law',
    '/civil-litigation':      'Civil Litigation',
    '/contract-disputes':     'Contract Disputes',
    '/real-estate-litigation': 'Real Estate Litigation',
    '/trust-probate':         'Trust & Probate Litigation',
}

GRUPOS = {
    '/employment-law': [
        'wrongful-termination', 'workplace-discrimination', 'sexual-harassment',
        'retaliation', 'unpaid-wages', 'severance-negotiation',
        'constructive-termination', 'paga-claims',
        'wrongful-termination-defense', 'retaliation-defense', 'wage-hour-defense',
        'paga-notice-response', 'hr-policies-handbooks', 'employment-contracts-severance',
    ],
    '/civil-litigation': [
        'breach-of-contract', 'breach-of-fiduciary-duty', 'business-fraud',
        'business-torts', 'llc-partnership-dissolution', 'shareholder-disputes',
    ],
    '/contract-disputes': [
        'misrepresentation-claims', 'non-compete-disputes', 'non-payment-disputes',
        'vendor-disputes',
    ],
    '/real-estate-litigation': [
        'adverse-possession', 'ccr-violations', 'co-ownership-disputes',
        'commercial-lease-disputes', 'easement-boundary-disputes', 'nuisance-claims',
        'real-estate-purchase-sale-disputes', 'realtor-fiduciary-duty',
    ],
    '/trust-probate': [
        'beneficiary-rights', 'conservatorship-disputes', 'contested-probate-matters',
        'trustee-breach-of-fiduciary-duty', 'trustee-removal', 'will-contests',
    ],
}

# Las de empleadores no se mezclan con las de empleados en "relacionadas": el
# lector de una es justo el contrario de la otra.
EMPLEADORES = {
    'wrongful-termination-defense', 'retaliation-defense', 'wage-hour-defense',
    'paga-notice-response', 'hr-policies-handbooks', 'employment-contracts-severance',
}

DE_QUIEN = {}
for madre, hijas in GRUPOS.items():
    for h in hijas:
        DE_QUIEN[h] = madre


def etiqueta(name):
    """El nombre corto de la pagina, tomado de su propia hero-pill."""
    ruta = name + '.html'
    if not os.path.exists(ruta):
        return name.replace('-', ' ').title()
    t = open(ruta, encoding='utf-8').read()
    m = re.search(r'class="hero-pill">([^<]*)', t)
    if not m:
        return name.replace('-', ' ').title()
    return m.group(1).split('·')[0].strip().replace('&amp;', '&')


def hermanas(name, cuantas=4):
    """Las vecinas mas cercanas, en el orden en que figuran en la madre."""
    madre = DE_QUIEN.get(name)
    if not madre:
        return []
    # Arranca despues de la propia pagina, para que cada una muestre vecinas
    # distintas y no todas apunten a las mismas cuatro.
    orden = GRUPOS[madre]
    corte = orden.index(name)
    rotado = orden[corte + 1:] + orden[:corte]
    if madre == '/employment-law':
        # Primero las del mismo lado, y si faltan se completa con el otro.
        rotado = ([h for h in rotado if (h in EMPLEADORES) == (name in EMPLEADORES)] +
                  [h for h in rotado if (h in EMPLEADORES) != (name in EMPLEADORES)])
    return rotado[:cuantas]
