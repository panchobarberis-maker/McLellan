// Barra de progreso de lectura. Misma logica que el snippet de Duda
// (duda-snippets/BARRA-PROGRESO.html): se crea sola, se estila desde JS y
// se esconde en paginas demasiado cortas para scrollear.
(function(){
  var ID = 'mlg-progreso';

  function estilos(barra){
    barra.style.cssText = [
      'position:fixed',
      'top:0',
      'left:0',
      'height:' + (window.innerWidth <= 768 ? '3px' : '4px'),
      'width:0',
      'margin:0',
      'padding:0',
      'border:0',
      'display:block',
      'opacity:1',
      'visibility:visible',
      'pointer-events:none',
      'z-index:2147483647',
      'background:linear-gradient(90deg,#c9a96e 0%,#e8cc8a 50%,#b8933a 100%)',
      'transition:width 0.1s linear'
    ].join(' !important;') + ' !important;';
  }

  // Cual es el elemento que scrollea. Casi siempre es la pagina entera, pero
  // si Duda mete un contenedor con scroll propio, lo usamos a el.
  function scroller(){
    var doc = document.documentElement;
    if (doc.scrollHeight - window.innerHeight > 40) return null; // null = ventana
    var todos = document.querySelectorAll('body *');
    for (var i = 0; i < todos.length; i++) {
      var el = todos[i];
      if (el.scrollHeight - el.clientHeight > 40) {
        var ov = getComputedStyle(el).overflowY;
        if (ov === 'auto' || ov === 'scroll') return el;
      }
    }
    return null;
  }

  function arrancar(){
    if (!document.body) return false;
    var barra = document.getElementById(ID);
    if (!barra) {
      barra = document.createElement('div');
      barra.id = ID;
      document.body.appendChild(barra);
    }
    estilos(barra);

    var caja = null;

    function pintar(){
      // Si algo del tema le pisa el estilo, se lo volvemos a poner.
      if (getComputedStyle(barra).position !== 'fixed') {
        var w = barra.style.width; estilos(barra); barra.style.width = w;
      }
      var alto, arriba, visible;
      if (caja) {
        alto = caja.scrollHeight; visible = caja.clientHeight; arriba = caja.scrollTop;
      } else {
        alto = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
        visible = window.innerHeight;
        arriba = window.scrollY || document.documentElement.scrollTop || 0;
      }
      var recorrido = alto - visible;
      // En paginas cortas no hay nada que medir: la barra se esconde.
      if (recorrido < 120) { barra.style.width = '0'; return; }
      barra.style.width = Math.max(0, Math.min(1, arriba / recorrido)) * 100 + '%';
    }

    function reconectar(){
      var nueva = scroller();
      if (nueva !== caja) {
        if (caja) caja.removeEventListener('scroll', pintar);
        caja = nueva;
        if (caja) caja.addEventListener('scroll', pintar, {passive:true});
      }
      pintar();
    }

    window.addEventListener('scroll', pintar, {passive:true});
    window.addEventListener('resize', function(){ estilos(barra); reconectar(); });
    window.addEventListener('load', reconectar);
    // Duda arma la pagina por partes: revisamos un rato hasta que se estabiliza.
    var n = 0, t = setInterval(function(){ reconectar(); if (++n > 20) clearInterval(t); }, 500);
    reconectar();
    return true;
  }

  if (!arrancar()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', arrancar);
    } else {
      var espera = setInterval(function(){ if (arrancar()) clearInterval(espera); }, 100);
    }
  }
})();
