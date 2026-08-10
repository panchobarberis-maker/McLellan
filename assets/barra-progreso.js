// Barra de progreso de lectura, vertical, pegada al borde derecho.
// Misma logica que el snippet de Duda (duda-snippets/BARRA-PROGRESO.html):
// se crea sola, se estila desde JS y se esconde en paginas demasiado cortas
// para scrollear.
//
// Son dos piezas: el riel, que muestra cuanto contenido hay en total, y el
// relleno, que crece a medida que se baja. Sin el riel no se entiende cuanto
// falta, que es justamente para lo que sirve.
(function(){
  var ID = 'mlg-progreso';

  function medidas(){
    var chico = window.innerWidth <= 768;
    return {
      ancho: chico ? '4px' : '6px',
      // Deja libres el header de arriba y un respiro abajo.
      arriba: chico ? '76px' : '96px',
      abajo: chico ? '24px' : '40px'
    };
  }

  function estilos(riel, relleno){
    var m = medidas();
    riel.style.cssText = [
      'position:fixed',
      'right:0',
      'top:' + m.arriba,
      'bottom:' + m.abajo,
      'width:' + m.ancho,
      'margin:0',
      'padding:0',
      'border:0',
      'border-radius:' + m.ancho,
      'overflow:hidden',
      'display:block',
      'opacity:1',
      'visibility:visible',
      'pointer-events:none',
      'z-index:2147483647',
      'background:rgba(140,148,150,0.35)'
    ].join(' !important;') + ' !important;';

    relleno.style.cssText = [
      'position:absolute',
      'top:0',
      'left:0',
      'right:0',
      'width:100%',
      'margin:0',
      'padding:0',
      'border:0',
      'border-radius:' + m.ancho,
      'display:block',
      'opacity:1',
      'visibility:visible',
      'pointer-events:none',
      'background:linear-gradient(180deg,#c9a96e 0%,#e8cc8a 50%,#b8933a 100%)',
      'transition:height 0.1s linear'
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
    var riel = document.getElementById(ID);
    var relleno;
    if (!riel) {
      riel = document.createElement('div');
      riel.id = ID;
      relleno = document.createElement('div');
      relleno.id = ID + '-relleno';
      riel.appendChild(relleno);
      document.body.appendChild(riel);
    } else {
      relleno = document.getElementById(ID + '-relleno');
    }
    estilos(riel, relleno);

    var caja = null;

    function pintar(){
      // Si algo del tema le pisa el estilo, se lo volvemos a poner.
      if (getComputedStyle(riel).position !== 'fixed') {
        var h = relleno.style.height; estilos(riel, relleno); relleno.style.height = h;
      }
      var alto, visible, arriba;
      if (caja) {
        alto = caja.scrollHeight; visible = caja.clientHeight; arriba = caja.scrollTop;
      } else {
        alto = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
        visible = window.innerHeight;
        arriba = window.scrollY || document.documentElement.scrollTop || 0;
      }
      var recorrido = alto - visible;
      // En paginas cortas no hay nada que medir: la barra se esconde entera.
      if (recorrido < 120) { riel.style.setProperty('display', 'none', 'important'); return; }
      riel.style.setProperty('display', 'block', 'important');
      relleno.style.height = Math.max(0, Math.min(1, arriba / recorrido)) * 100 + '%';
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
    window.addEventListener('resize', function(){ estilos(riel, relleno); reconectar(); });
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
