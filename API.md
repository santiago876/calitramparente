# Integración de la API

La vista de Banderas Rojas accede a datos a través de `src/services/redFlags.js`; los componentes no realizan solicitudes HTTP directamente. El cliente compartido está en `src/api/client.js`.

## Configuración local

1. Copia `.env.example` como `.env.local`.
2. Configura la raíz del backend en `VITE_API_BASE_URL`.
3. Cambia `VITE_DATA_SOURCE` a `api` y ajusta `VITE_RED_FLAGS_ENDPOINT` a la ruta implementada por el backend.
4. Reinicia Vite después de modificar las variables de entorno.

Con `VITE_DATA_SOURCE=mock` se usan los ejemplos ficticios locales. En modo `api` los errores de conexión, HTTP y formato se muestran en la vista; no se sustituyen silenciosamente por datos de demostración.

## Contrato esperado para Banderas Rojas

El endpoint responde con una lista JSON:

```json
[
  {
    "id": "CONTRATO-123",
    "entidad": "Secretaría de Infraestructura",
    "objeto": "Mantenimiento de vías",
    "contratista": "Empresa contratista",
    "valor": "$120 millones",
    "fecha": "2026-08-18",
    "tipo": "Adición presupuestal",
    "riesgo": "alto",
    "descripcion": "Descripción de la señal detectada",
    "detalle": "Contexto y documentos que se recomienda revisar"
  }
]
```

También se aceptan respuestas envueltas como `{"items": [...]}` o `{"data": [...]}`. `riesgo` admite `alto`, `medio` o `bajo`; `detalle` es opcional. Los demás campos del ejemplo son requeridos y deben ser texto, excepto `id`, que puede ser texto o número.

Si el frontend y la API tienen distintos orígenes, el backend debe permitir mediante CORS el origen del frontend. Para desarrollo local, el backend debe permitir `http://localhost:5173` (o el puerto que use Vite).

## Alcance actual

Esta primera integración conecta la sección de Banderas Rojas. El mapa y las tarjetas resumen todavía usan datos locales de `src/data/comunas.js`; se pueden conectar mediante servicios adicionales cuando se definan sus endpoints y contratos.
