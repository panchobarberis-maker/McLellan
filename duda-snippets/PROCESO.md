# Cómo publicar cada subpágina

## Qué va en Duda y qué va en el HTML

El widget se inserta en el **cuerpo** de la página, no en el `<head>`. Un
`<title>` o una `<meta description>` puestos en el cuerpo **Google los ignora**.
Por eso no es opcional:

| Dato | Dónde | Por qué |
|---|---|---|
| **Title** | Panel de Duda | En el cuerpo no lo lee nadie |
| **Description** | Panel de Duda | Ídem |
| **Open Graph** | Panel de Duda | Ídem |
| **Canonical** | Lo genera Duda | No hay campo, sale de la URL |
| **FAQPage** (schema) | Dentro del widget | El JSON-LD sí vale en el cuerpo |
| **Diseño y contenido** | Dentro del widget | |

No hay riesgo de contradicción: **el archivo `-COMPLETO.html` no trae ninguna
meta tag** (verificado: cero `<title>`, cero `description`, cero `canonical`).
Cada dato existe en un solo lugar.

## Una sola vez, antes de todo

1. **Sacar del head del sitio** el `<link rel="canonical">` y los seis `og:`.
   Mientras estén, marcan cada página como copia del home y nada de lo demás
   sirve.
2. **Dejar un solo bloque `LegalService`** en el head: el que tiene `sameAs`.
3. **Dejar Wrongful Termination como plantilla** en Duda.

## Por cada una de las 37 restantes

1. **Duplicar Wrongful Termination** en Duda. Hereda el ROW en full bleed, los
   paddings, los colores y el ajuste del logo en mobile.
2. **Cambiar el slug** al que figura en `SLUGS.md`.
3. **Reemplazar el contenido del widget** por su `-COMPLETO.html`.
4. **Page Settings → SEO**: pegar Title y Description de `META-TAGS-DUDA.md`.
5. **Destildar "Set page to no index"**.
6. **Header HTML: vacío.** El schema ya viaja en el widget.
7. **Publicar** y abrir la URL.

Son siete pasos y ninguno necesita tocar código.

## Cuando estén las 38

8. **Employment Law y las otras 5 madre**: sus links a las subpáginas ya
   apuntan a las URL definitivas.
9. **Menú**: agregar las páginas. Ojo con mobile, que en este sitio no hereda
   del menú de desktop.
10. **Sitemap**: regenerarlo desde Duda.
11. **Search Console**: enviar el sitemap y pedir indexación.

## Verificar en la primera que publiques

- Ver el código fuente y buscar `canonical`: tiene que haber **uno solo**, y
  apuntando a esa misma página.
- Buscar `application/ld+json`: **dos bloques**, un `LegalService` (del sitio)
  y un `FAQPage` (de la página).
- Probar la URL en el Rich Results Test de Google.
