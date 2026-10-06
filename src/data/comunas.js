// riesgo: 'bajo' | 'medio' | 'alto'. Reemplazar por datos de la API FastAPI.
// Orden = disposición de la cuadrícula del diseño (5 columnas).
const z = (id, alertas, riesgo, extra = {}) => ({ id, nombre: id, alertas, riesgo, ...extra })

export const zonas = [
  z('C1', 1, 'bajo'), z('C2', 0, 'bajo'), z('C7', 0, 'bajo'), z('C19', 1, 'medio'), z('C22', 0, 'bajo'),
  z('C8', 2, 'medio'), z('C6', 1, 'bajo'), z('C5', 2, 'medio'), z('C18', 2, 'medio'), z('C17', 3, 'alto'),
  z('C9', 0, 'bajo'), z('C3', 3, 'alto'), z('C4', 1, 'medio'), z('C10', 1, 'bajo'), z('C16', 1, 'bajo'),
  z('C11', 1, 'medio'), z('C12', 0, 'bajo'), z('C13', 0, 'bajo'), z('C14', 0, 'bajo'), z('C15', 4, 'alto'),
  // Fila parcialmente visible en la captura: ajustar al diseño final
  z('C20', 5, 'alto'), z('C21', 0, 'bajo'),
  z('Rural Norte', 0, 'bajo', { tipo: 'Zona Rural' }),
  z('Corregimiento Sur', 0, 'bajo', {
    tipo: 'Zona Rural', contratos: 4, invertido: '780 M',
    secretarias: ['Infraestructura Rural'], proyectos: ['Vías Rurales Sur'],
  }),
]

export const resumen = {
  presupuesto: '$0.1 Bill.', contratos: 298, secretarias: 12,
  auditados: 241, cobertura: 81, banderas: 31, adicionProm: 18.4,
}
