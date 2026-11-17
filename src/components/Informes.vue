<script setup>
import { computed } from 'vue'
import { BarChart3, CircleDollarSign, FileText, ShieldAlert } from 'lucide-vue-next'
import { contratos } from '../data/contratos'

const cantidad = contratos.length
const valorTotal = computed(() => contratos.reduce((total, item) => {
  const valor = Number(item.valor.replace(/\D/g, ''))
  return total + (Number.isFinite(valor) ? valor : 0)
}, 0))

const formatoMoneda = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  maximumFractionDigits: 0,
})

const porRiesgo = computed(() => [
  { nombre: 'Alto', clave: 'alto', cantidad: contratos.filter(item => item.riesgo === 'alto').length },
  { nombre: 'Medio', clave: 'medio', cantidad: contratos.filter(item => item.riesgo === 'medio').length },
  { nombre: 'Bajo', clave: 'bajo', cantidad: contratos.filter(item => item.riesgo === 'bajo').length },
])

const porEstado = computed(() => ['En ejecución', 'Vigente', 'Cerrado'].map(nombre => ({
  nombre,
  cantidad: contratos.filter(item => item.estado === nombre).length,
})))

const porTipo = computed(() => {
  const conteo = contratos.reduce((total, item) => {
    total[item.tipo] = (total[item.tipo] ?? 0) + 1
    return total
  }, {})

  return Object.entries(conteo)
    .map(([nombre, total]) => ({ nombre, cantidad: total }))
    .sort((a, b) => b.cantidad - a.cantidad || a.nombre.localeCompare(b.nombre))
})

const porcentaje = total => cantidad ? Math.round((total / cantidad) * 100) : 0
</script>

<template>
  <section class="reports-page">
    <header class="intro">
      <div>
        <span class="eyebrow"><BarChart3 :size="16" /> INFORMES</span>
        <h1>Informes y estadísticas</h1>
        <p>Resumen de los contratos incluidos en esta plataforma, organizado por valor, riesgo, estado y tipo.</p>
      </div>
    </header>

    <aside class="demo-note" role="note">
      <ShieldAlert :size="18" />
      <p><strong>Informe de demostración.</strong> Las cifras se calculan a partir de los contratos ficticios de ejemplo disponibles en esta versión; no representan la contratación pública real de Cali.</p>
    </aside>

    <section class="metrics" aria-label="Indicadores del conjunto de muestra">
      <article class="metric card">
        <span class="metric-icon blue"><FileText :size="21" /></span>
        <div><small>CONTRATOS EN MUESTRA</small><strong>{{ cantidad }}</strong><p>Registros de ejemplo</p></div>
      </article>
      <article class="metric card">
        <span class="metric-icon green"><CircleDollarSign :size="21" /></span>
        <div><small>VALOR TOTAL EN MUESTRA</small><strong>{{ formatoMoneda.format(valorTotal) }}</strong><p>Suma de los valores de ejemplo</p></div>
      </article>
      <article class="metric card">
        <span class="metric-icon red"><ShieldAlert :size="21" /></span>
        <div><small>RIESGO ALTO</small><strong>{{ porRiesgo[0].cantidad }}</strong><p>{{ porcentaje(porRiesgo[0].cantidad) }}% de la muestra</p></div>
      </article>
    </section>

    <section class="charts" aria-label="Desglose de contratos">
      <article class="card chart-card">
        <div class="chart-heading">
          <div><h2>Contratos por nivel de riesgo</h2><p>Distribución de los registros de muestra</p></div>
        </div>
        <div class="bars">
          <div v-for="item in porRiesgo" :key="item.clave" class="bar-row">
            <span class="bar-label">{{ item.nombre }}</span>
            <div class="bar-track">
              <div class="bar-fill" :class="item.clave" role="progressbar"
                :aria-label="`${item.nombre}: ${item.cantidad} contratos`"
                :aria-valuenow="item.cantidad" :aria-valuemin="0" :aria-valuemax="cantidad"
                :style="{ width: `${porcentaje(item.cantidad)}%` }"></div>
            </div>
            <strong>{{ item.cantidad }}</strong>
          </div>
        </div>
      </article>

      <article class="card chart-card">
        <div class="chart-heading">
          <div><h2>Contratos por estado</h2><p>Estado registrado en cada ejemplo</p></div>
        </div>
        <div class="bars">
          <div v-for="item in porEstado" :key="item.nombre" class="bar-row">
            <span class="bar-label">{{ item.nombre }}</span>
            <div class="bar-track">
              <div class="bar-fill status" role="progressbar"
                :aria-label="`${item.nombre}: ${item.cantidad} contratos`"
                :aria-valuenow="item.cantidad" :aria-valuemin="0" :aria-valuemax="cantidad"
                :style="{ width: `${porcentaje(item.cantidad)}%` }"></div>
            </div>
            <strong>{{ item.cantidad }}</strong>
          </div>
        </div>
      </article>

      <article class="card chart-card type-chart">
        <div class="chart-heading">
          <div><h2>Contratos por tipo</h2><p>Clasificación de los registros incluidos</p></div>
        </div>
        <div class="bars">
          <div v-for="item in porTipo" :key="item.nombre" class="bar-row">
            <span class="bar-label">{{ item.nombre }}</span>
            <div class="bar-track">
              <div class="bar-fill type" role="progressbar"
                :aria-label="`${item.nombre}: ${item.cantidad} contratos`"
                :aria-valuenow="item.cantidad" :aria-valuemin="0" :aria-valuemax="cantidad"
                :style="{ width: `${porcentaje(item.cantidad)}%` }"></div>
            </div>
            <strong>{{ item.cantidad }}</strong>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<style scoped>
.reports-page { padding: 36px 0 32px; }
.intro { margin-bottom: 24px; }
.eyebrow { display: inline-flex; align-items: center; gap: 8px; color: var(--navy); font-size: 12px; font-weight: 700; letter-spacing: .1em; }
h1 { margin: 10px 0 8px; color: var(--ink); font-size: 32px; font-weight: 600; }
.intro p { max-width: 700px; margin: 0; color: var(--muted); line-height: 1.6; }
.demo-note { display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; margin-bottom: 20px; border: 1px solid #f2d9ae; border-radius: 10px; background: #fff9ed; color: #8a5300; }
.demo-note svg { flex: none; margin-top: 2px; }
.demo-note p { margin: 0; font-size: 13px; line-height: 1.55; }
.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
.metric { display: flex; align-items: flex-start; gap: 16px; padding: 22px; }
.metric-icon { display: grid; place-items: center; flex: none; width: 46px; height: 46px; border-radius: 11px; }
.metric-icon.blue { background: #e8f0fb; color: var(--navy); }
.metric-icon.green { background: var(--green-bg); color: var(--green); }
.metric-icon.red { background: var(--red-bg); color: var(--red); }
.metric small { display: block; color: var(--muted); font-size: 11px; font-weight: 700; letter-spacing: .08em; }
.metric strong { display: block; margin: 5px 0; color: var(--ink); font-size: 25px; overflow-wrap: anywhere; }
.metric p { margin: 0; color: var(--muted); font-size: 13px; }
.charts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin-top: 20px; }
.chart-card { padding: 22px; }
.type-chart { grid-column: 1 / -1; }
.chart-heading h2 { margin: 0; color: var(--ink); font-size: 18px; font-weight: 600; }
.chart-heading p { margin: 6px 0 0; color: var(--muted); font-size: 13px; }
.bars { display: grid; gap: 18px; margin-top: 24px; }
.bar-row { display: grid; grid-template-columns: minmax(100px, 150px) minmax(60px, 1fr) 28px; align-items: center; gap: 12px; }
.bar-label { color: var(--ink); font-size: 14px; }
.bar-track { height: 12px; overflow: hidden; border-radius: 99px; background: #edf1f6; }
.bar-fill { height: 100%; min-width: 0; border-radius: inherit; transition: width .2s ease; }
.bar-fill.alto { background: var(--red); }
.bar-fill.medio { background: var(--amber); }
.bar-fill.bajo { background: var(--green); }
.bar-fill.status { background: var(--navy); }
.bar-fill.type { background: #4a86c5; }
.bar-row strong { color: var(--ink); font-size: 14px; text-align: right; }
@media (max-width: 700px) {
  .reports-page { padding-top: 26px; }
  .charts { grid-template-columns: 1fr; }
  .type-chart { grid-column: auto; }
  .chart-card { padding: 18px 14px; }
  .bar-row { grid-template-columns: minmax(86px, 120px) minmax(40px, 1fr) 22px; gap: 8px; }
  .bar-label { font-size: 12px; }
}
</style>
