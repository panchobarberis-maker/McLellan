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

## Video de fondo del hero: NO usar script de carga

Versión vieja (rota): dos `<video>` con `data-src` en vez de `src`, más un
`<script>` que elegía cuál video cargar según el ancho de pantalla usando
`document.currentScript.closest(".emp-hero")`. Duda mueve ese script fuera
de `.emp-hero` al armar el widget, `closest()` no lo encuentra, y como es
el primer statement de un bloque `<script>` que también arma el sistema de
reveal (la animación de aparición) y el carousel de testimonios, el error
aborta TODO el bloque: video que no carga, texto que nunca aparece, FAQ que
no abre. Pasó en `/retaliation`, `/sexual-harassment` y
`/severance-negotiation` recién pegadas y probablemente en cualquier
página que se vuelva a generar con el patrón viejo.

Versión correcta (la que hay que usar siempre): los dos `<video>` con
`src` directo (no `data-src`) y `autoplay`, sin ningún script asociado.
El CSS del Site Head (`.mlgP .video-mobile { display:none }` +
`@media(max-width:768px)`) ya se encarga de mostrar el que corresponde
según el tamaño de pantalla. No hace falta JS para esto.

```html
<video class="emp-hero-img video-desktop" autoplay muted loop playsinline preload="auto"><source src="URL_DESKTOP" type="video/mp4"></video><video class="emp-hero-img video-mobile" autoplay muted loop playsinline preload="auto"><source src="URL_MOBILE" type="video/mp4"></video>
```

Si en algún momento se arma una página nueva a mano (copiando otra vieja
como base), verificar que el hero no tenga el script viejo. Buscar
`document.currentScript` en el archivo: si aparece, hay que sacarlo.
