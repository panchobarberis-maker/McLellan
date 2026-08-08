# Migrar de Vercel a Duda sin romper el SEO

## El orden importa: primero las subpáginas, después la madre

Employment Law enlaza a sus 14 subpáginas, y las subpáginas enlazan de vuelta a
Employment Law.

- **Employment Law ya existe en producción**, así que los links de las subpáginas
  hacia ella funcionan desde el minuto cero.
- Si publicás la madre primero, sus 14 links apuntan a páginas que todavía no
  existen: 14 errores 404 que Google puede rastrear antes de que los arregles.

Por eso: **las 14 subpáginas primero, la madre al final.**

## Los slugs ya están decididos

Los links internos del markup salen apuntando a la URL final de Duda, no a
rutas de Vercel. La tabla vive en `build-widget.py`:

| Vercel | Duda |
|---|---|
| `wrongful-termination.html` | `/wrongful-termination` |
| `business-litigation.html` | `/civil-litigation` |
| `contact.html` | `/contact-us` |
| `index.html` | `/` |
| el resto | igual que el nombre del archivo |

**Al crear cada página en Duda, el slug tiene que coincidir exactamente con
esta tabla.** Si Duda te obliga a otro, avisá: se cambia la tabla, se regeneran
todas de una y no hay que tocar ningún link a mano.

## Por cada subpágina

1. **Crear la página** en Duda con el slug exacto (`/wrongful-termination`).
2. **Configurar el ROW**: full bleed, padding 0, fondo `#1e3a3e`.
3. **Configurar la COLUMN**: padding 0, fondo `#1e3a3e`.
4. **Pegar el CSS** (widget arriba, o una sola vez en el head del sitio).
5. **Pegar el markup** en un widget debajo.
6. **Pegar el schema** en otro widget, en cualquier posición.
7. **Cargar Title y Meta description** desde Page Settings → SEO.
   Están en `SEO-subpaginas.md`, copiados de las páginas de Vercel.
8. **Canonical**: que apunte a sí misma, `https://www.mclellanlawgroup.com/<slug>`.
   Nunca al home.
9. **Publicar** y abrir la URL para confirmar que responde.

## Cuando estén las 14

10. **Employment Law**: pegar su markup nuevo, que ya trae los 14 links con las
    URL definitivas.
11. **Menú**: agregar las subpáginas donde corresponda. Ojo con el menú de
    mobile, que en este sitio no hereda del de desktop.
12. **Sitemap**: regenerarlo desde Duda para que incluya las nuevas.
13. **Search Console**: mandar el sitemap y pedir indexación de la madre.

## Revisar antes de dar por cerrado

- **El canonical del head del sitio.** Hoy hay uno apuntando al home aplicado a
  todas las páginas. Mientras esté, Google trata cada página como copia del home
  y no la indexa por separado. Es lo más urgente de esta lista.
- **Los tags `og:`** del head del sitio: mismo problema, título y URL del home
  en todas las páginas.
- **`landed_url` de Lawbrokr**: cada página reporta la suya. Ya está resuelto en
  el repo, pero verificar que el widget pegado sea el actualizado.

## Lo que no hay que hacer

- **No publicar las páginas de Vercel.** Siguen con `noindex` y `robots.txt` en
  `Disallow: /`. Son preview.
- **No dejar dos URLs con el mismo contenido** sin canonical entre ellas.
- **No cambiar un slug después de publicar** sin dejar una redirección 301.
