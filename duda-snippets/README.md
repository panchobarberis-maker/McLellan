# Qué se pega en Duda

Esta carpeta tiene siempre la **última versión** de todo lo que va a Duda. Si un
archivo está acá, es el bueno.

## Los tres archivos que se pegan

| Archivo | Dónde va | Cuántas veces |
|---|---|---|
| `SITE-HEAD.html` | Site Settings → Head HTML | 1 vez en todo el sitio |
| `<pagina>-MARKUP.html` | Widget HTML en el cuerpo de la página | 1 por página |
| `<pagina>-SCHEMA.html` | Otro widget, en cualquier posición | 1 por página |

`SITE-HEAD.html` ya viene armado y completo. Se reemplaza entero, de la primera
línea a la última. Adentro trae, en este orden:

1. El head original del sitio: viewport, usestyle.ai, verificación de Google y
   Bing, favicons, `robots`, Flodesk.
2. La ficha `LegalService`, una sola vez.
3. La barra de progreso de lectura.
4. El CSS de las 38 subpáginas, todo acotado a `.mlgP`.

`practice-CSS-COMUN.html` es solo el punto 4, por si alguna vez conviene pegar
ese bloque suelto en vez del head entero. No hay que pegar los dos.

## Lo que NO va en Duda

- **Title y meta description**: se cargan en Page Settings → SEO. Están en
  `META-TAGS-DUDA.md`. En el cuerpo Google no las lee.
- **Canonical**: lo genera Duda solo.
- **Header HTML de la página**: vacío. El schema ya viaja en su widget.

## Que hay que volver a pegar

    python3 duda-snippets/cambios.py            lo que cambio
    python3 duda-snippets/cambios.py --pegado   marcar todo como ya pegado

El contenido vive dentro de un widget HTML, asi que Duda no deja editar una
palabra desde el editor: cualquier cambio de texto obliga a regenerar y pegar
de nuevo. Lo unico que se puede hacer es pegar lo minimo, y para eso hay que
saber que cambio de verdad. Los comentarios no cuentan.

## Los generadores

    python3 duda-snippets/build-practice.py wrongful-termination.html --css

Con `--css` también emite el CSS común y **compara las 38 páginas contra él**.
Si imprime algún `OJO`, esa página tiene una regla que el head no cubre y se
vería mal en Duda. Con 0 desvíos, el head sirve para las 38.

`enlaces.py` dice a qué práctica pertenece cada subpágina. De ahí salen el
breadcrumb y el bloque de páginas relacionadas.

## Documentos

- `PROCESO.md`: los pasos para publicar cada subpágina.
- `CHECKLIST-MIGRACION.md`: el orden de la migración y las reglas de SEO.
- `SLUGS.md`: las URL definitivas.
- `META-TAGS-DUDA.md`: title y description de las 38.
- `VIDEOS.md`: los links del hero en el Media Manager.
