import { getJson } from '../api/client'
import { banderas as datosDemo } from '../data/banderas'

const fuente = import.meta.env.VITE_DATA_SOURCE?.trim().toLowerCase() || 'mock'
const endpoint = import.meta.env.VITE_RED_FLAGS_ENDPOINT?.trim() || '/red-flags'

const riesgosValidos = new Set(['alto', 'medio', 'bajo'])
const camposTexto = ['entidad', 'objeto', 'contratista', 'valor', 'fecha', 'tipo', 'descripcion']

export const usaDatosDemo = fuente === 'mock'

function normalizarAlerta(alerta, indice) {
  if (!alerta || typeof alerta !== 'object' || Array.isArray(alerta)) {
    throw new Error(`La alerta en la posición ${indice} tiene un formato inválido.`)
  }

  if (alerta.id === undefined || alerta.id === null || String(alerta.id).trim() === '') {
    throw new Error(`La alerta en la posición ${indice} no tiene un identificador.`)
  }

  for (const campo of camposTexto) {
    if (typeof alerta[campo] !== 'string') {
      throw new Error(`El campo "${campo}" de la alerta ${alerta.id} debe ser texto.`)
    }
  }

  if (!riesgosValidos.has(alerta.riesgo)) {
    throw new Error(`La alerta ${alerta.id} tiene un riesgo inválido; use alto, medio o bajo.`)
  }

  if (alerta.detalle !== undefined && typeof alerta.detalle !== 'string') {
    throw new Error(`El campo "detalle" de la alerta ${alerta.id} debe ser texto.`)
  }

  return {
    id: String(alerta.id),
    entidad: alerta.entidad,
    objeto: alerta.objeto,
    contratista: alerta.contratista,
    valor: alerta.valor,
    fecha: alerta.fecha,
    tipo: alerta.tipo,
    riesgo: alerta.riesgo,
    descripcion: alerta.descripcion,
    detalle: alerta.detalle ?? '',
  }
}

function extraerLista(payload) {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.items)) return payload.items
  if (Array.isArray(payload?.data)) return payload.data

  throw new Error('La respuesta de banderas rojas debe ser una lista o contener "items" o "data".')
}

export async function obtenerBanderasRojas(options) {
  if (fuente === 'mock') {
    return datosDemo
  }

  if (fuente !== 'api') {
    throw new Error(`VITE_DATA_SOURCE debe ser "mock" o "api"; se recibió "${fuente}".`)
  }

  const payload = await getJson(endpoint, options)
  return extraerLista(payload).map(normalizarAlerta)
}
