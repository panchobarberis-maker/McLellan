# Videos del hero — fuente única

Todo hero con video usa **estas dos URLs y ninguna otra**. Valen igual en Vercel y
en Duda, así que un bloque copiado de una página a la otra funciona sin tocar nada.

**Desktop**

```
https://vid.cdn-website.com/9df80dfc/videos/RvNk8sW9RoeNLVMnGe2t_video-mclellan-para-duda-v.mp4
```

**Mobile**

```
https://vid.cdn-website.com/9df80dfc/videos/v6p2xYTECGVqRjvAzOkw_video-mclellan-mobile-para-duda-CORRECTO-v.mp4
```

## Bloque a copiar

```html
<video class="video-desktop" autoplay muted loop playsinline preload="auto">
  <source src="https://vid.cdn-website.com/9df80dfc/videos/RvNk8sW9RoeNLVMnGe2t_video-mclellan-para-duda-v.mp4" type="video/mp4">
</video>
<video class="video-mobile" autoplay muted loop playsinline preload="auto">
  <source src="https://vid.cdn-website.com/9df80dfc/videos/v6p2xYTECGVqRjvAzOkw_video-mclellan-mobile-para-duda-CORRECTO-v.mp4" type="video/mp4">
</video>
```

`autoplay muted loop playsinline` van los cuatro juntos: sin `muted` y sin
`playsinline` iOS no arranca solo, y sin `playsinline` lo abre en pantalla completa.

## Reglas

- **No usar rutas relativas** (`src="video mclellan.mp4"`). Funcionan en Vercel y
  se rompen apenas el bloque se pega en Duda.
- **No usar `raw.githubusercontent.com`.** Devuelve `application/octet-stream` con
  `x-content-type-options: nosniff`, así que el navegador se niega a decodificar el
  mp4 y el hero queda sin video. Fue la causa del bug del Widget 1.
- **Siempre `type="video/mp4"` en el `<source>`.** Evita depender del `Content-Type`
  que mande el CDN.
- **Nunca apagar el video por scroll.** Un `classList.add('is-hidden')` disparado con
  `{once:true}` deja el video en `opacity:0` para siempre, y Duda restaura la posición
  de scroll al recargar el preview, así que se apaga antes de aparecer. Fue el bug del
  hero del newsletter.

## Si cambian los videos

Se reemplazan en el Media Manager de Duda, se actualizan las dos URLs de acá y se
corren sobre todos los `.html` del repo. Un solo par de links, un solo lugar donde
tocarlos.
