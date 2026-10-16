const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim().replace(/\/+$/, '')

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function getJson(path, { signal } = {}) {
  if (!apiBaseUrl) {
    throw new Error('Falta configurar VITE_API_BASE_URL para usar la API.')
  }

  const endpoint = new URL(path.replace(/^\/+/, ''), `${apiBaseUrl}/`)
  const response = await fetch(endpoint, {
    headers: { Accept: 'application/json' },
    signal,
  })

  if (!response.ok) {
    const responseText = await response.text()
    let message = responseText

    try {
      const body = JSON.parse(responseText)
      message = body.detail ?? body.message ?? responseText
    } catch {
      message = responseText
    }

    throw new ApiError(
      `La API respondió ${response.status}${message ? `: ${message}` : ''}`,
      response.status,
    )
  }

  try {
    return await response.json()
  } catch {
    throw new Error('La API respondió con un JSON inválido.')
  }
}
