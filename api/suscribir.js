// Recibe el email de la calculadora y lo manda a Flodesk, al segmento que
// corresponde segun el perfil que eligio la persona.
//
// Existe por una razon concreta: el formulario embebido de Flodesk trae su
// propio diseno y no se puede integrar a la tarjeta de la calculadora. Con
// esto la casilla es nuestra y Flodesk solo recibe el dato.
//
// La clave de Flodesk NUNCA puede estar en el navegador, por eso esto corre
// en el servidor. Se configura en Vercel, en Settings, Environment Variables:
//
//   FLODESK_API_KEY        la clave de la API de Flodesk
//   SEGMENTO_INDIVIDUAL    id del segmento general
//   SEGMENTO_ATTORNEY      id del segmento de abogados
//   SEGMENTO_PROFESIONAL   id del segmento de otros profesionales
//
// Si en lugar de la API preferis pasar por Zapier o Make, alcanza con definir
// WEBHOOK_URL y se reenvia ahi sin tocar Flodesk.

const SEGMENTOS = {
  individual:  process.env.SEGMENTO_INDIVIDUAL,
  attorney:    process.env.SEGMENTO_ATTORNEY,
  profesional: process.env.SEGMENTO_PROFESIONAL,
};

// La pagina tambien vive en Duda, asi que la llamada llega de otro dominio.
const PERMITIDOS = [
  'https://mc-lellan.vercel.app',
  'https://www.mclellanlawgroup.com',
  'https://mclellanlawgroup.com',
];

function cors(req, res) {
  const origen = req.headers.origin;
  if (PERMITIDOS.includes(origen)) res.setHeader('Access-Control-Allow-Origin', origen);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

export default async function handler(req, res) {
  cors(req, res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { email, name, who } = req.body || {};
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: 'A valid email is required.' });
  }

  // Camino alternativo: reenviar a Zapier, Make o similar.
  if (process.env.WEBHOOK_URL) {
    try {
      await fetch(process.env.WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name, who, tool: 'interest-calculator' }),
      });
      return res.status(200).json({ ok: true });
    } catch (e) {
      return res.status(502).json({ error: 'Could not reach the subscription service.' });
    }
  }

  const clave = process.env.FLODESK_API_KEY;
  if (!clave) return res.status(501).json({ error: 'Subscriptions are not configured yet.' });

  // Flodesk autentica con Basic, usando la clave como usuario y sin password.
  const auth = 'Basic ' + Buffer.from(clave + ':').toString('base64');
  const cabeceras = { 'Content-Type': 'application/json', Authorization: auth };

  try {
    const alta = await fetch('https://api.flodesk.com/v1/subscribers', {
      method: 'POST',
      headers: cabeceras,
      body: JSON.stringify({
        email,
        first_name: (name || '').split(' ')[0] || undefined,
        last_name: (name || '').split(' ').slice(1).join(' ') || undefined,
        custom_fields: { source: 'interest-calculator', profile: who || 'unknown' },
      }),
    });
    if (!alta.ok && alta.status !== 409) {
      return res.status(502).json({ error: 'The subscription service rejected the request.' });
    }

    const segmento = SEGMENTOS[who];
    if (segmento) {
      await fetch(`https://api.flodesk.com/v1/subscribers/${encodeURIComponent(email)}/segments`, {
        method: 'POST',
        headers: cabeceras,
        body: JSON.stringify({ segment_ids: [segmento] }),
      });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(502).json({ error: 'Could not reach the subscription service.' });
  }
}
