import { postJson } from '../api/client'

const endpoint = import.meta.env.VITE_REPORTS_ENDPOINT?.trim() || '/reports'

export async function enviarReporte(reporte, options) {
  return postJson(endpoint, reporte, options)
}
