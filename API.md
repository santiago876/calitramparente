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

La sección de Informes agrega métricas a partir de los contratos de ejemplo en `src/data/contratos.js`. Sus cifras son demostrativas y no datos oficiales; la sección debe conectarse a un endpoint de contratos antes de usarse como fuente de análisis real.

## Recepción de reportes ciudadanos

El botón **Reportar** abre un formulario que envía un `POST` JSON al endpoint relativo configurado en `VITE_REPORTS_ENDPOINT` (por defecto `/reports`), usando `VITE_API_BASE_URL`. El backend debe aceptar el siguiente cuerpo y responder con un estado HTTP 2xx para confirmar la recepción:

```json
{
  "contract_id": "SECOP-II-12345",
  "category": "Posible sobrecosto o adición",
  "description": "Descripción de lo observado, con al menos 20 caracteres.",
  "reporter_name": null,
  "reporter_email": null
}
```

`contract_id`, `reporter_name` y `reporter_email` pueden ser `null`; `category` y `description` son obligatorios. El backend debe validar los datos, proteger contra abuso, almacenar los reportes de forma segura y definir su política de privacidad y retención. Si el API usa otro origen, debe permitir mediante CORS el origen del frontend.

### Backend local

Se agregó un backend FastAPI en `backend/` que guarda reportes en SQLite, en `backend/reports.db` por defecto. Para ejecutarlo en Windows PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000/api/v1/reports`; la verificación de estado está en `/api/v1/health` y la documentación interactiva de FastAPI en `/docs`. `REPORTS_DB_PATH` permite cambiar el archivo SQLite y `CORS_ORIGINS` configura los orígenes permitidos, separados por comas. El frontend local usa `.env.local` para enviar al servidor de desarrollo; reinicia Vite tras cambiar esa configuración.

Para ejecutar las pruebas desde `backend/`, instala los requisitos y corre `pytest`. Antes de publicar el formulario a internet, agrega controles de abuso (por ejemplo, rate limiting y/o CAPTCHA), decide quién revisará los reportes y establece una política de privacidad y retención. Esta primera versión no incluye una bandeja administrativa ni autenticación para consultar reportes.

### Publicación de demostración

Esta configuración es solo para una demostración: no envíes reportes reales ni datos personales. El servicio gratuito de Render puede apagarse cuando queda inactivo y su sistema de archivos es temporal; los reportes guardados en `/tmp/reports.db` pueden perderse al reiniciar o desplegar. Para conservar reportes, configura una base de datos persistente antes de aceptar envíos reales.

#### API en Render

1. En Render, crea un **Blueprint** desde este repositorio y acepta la configuración de `render.yaml`.
2. Render solicitará `CORS_ORIGINS`; configúralo con el origen de producción de Vercel (por ejemplo, `https://tu-proyecto.vercel.app`, sin barra final). Si aún no tienes ese dominio, créalo primero en Vercel y luego configura esta variable desde el panel de Render.
3. Espera a que termine el despliegue. La API será `https://<nombre-del-servicio>.onrender.com`; verifica `/api/v1/health`.

#### Frontend en Vercel

1. Importa este repositorio en Vercel. Usa la raíz del repositorio, el comando `npm run build` y el directorio de salida `dist`.
2. Crea el despliegue para obtener el dominio de producción de Vercel.
3. En las variables de entorno de producción, define `VITE_API_BASE_URL` como `https://<nombre-del-servicio>.onrender.com/api/v1` y despliega de nuevo.
4. Vuelve a Render y configura `CORS_ORIGINS` con el dominio de producción de Vercel.

El frontend también conserva la publicación de GitHub Pages: el workflow define `VITE_BASE_PATH=/calitramparente/`; Vercel usa `/` por defecto.
