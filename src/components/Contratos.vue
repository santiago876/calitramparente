<script setup>
import { computed, nextTick, ref } from 'vue'
import { ArrowRight, FileText, Search, ShieldAlert, X } from 'lucide-vue-next'
import { contratos } from '../data/contratos'

const busqueda = ref('')
const riesgo = ref('todos')
const estado = ref('todos')
const contratoActivo = ref(null)
const botonCerrar = ref(null)
const focoAnterior = ref(null)

const opcionesRiesgo = ['todos', 'alto', 'medio', 'bajo']
const opcionesEstado = ['todos', 'En ejecución', 'Vigente', 'Cerrado']

const visibles = computed(() => {
  const texto = busqueda.value.trim().toLowerCase()

  return contratos.filter(item => {
    const coincideTexto = !texto || `${item.id} ${item.objeto} ${item.entidad} ${item.contratista} ${item.comuna}`.toLowerCase().includes(texto)
    const coincideRiesgo = riesgo.value === 'todos' || item.riesgo === riesgo.value
    const coincideEstado = estado.value === 'todos' || item.estado === estado.value
    return coincideTexto && coincideRiesgo && coincideEstado
  })
})

const totalPorRiesgo = nivel => contratos.filter(item => item.riesgo === nivel).length
async function abrirContrato(item) {
  focoAnterior.value = document.activeElement
  contratoActivo.value = item
  await nextTick()
  botonCerrar.value?.focus()
}

async function cerrarContrato() {
  contratoActivo.value = null
  await nextTick()
  focoAnterior.value?.focus()
  focoAnterior.value = null
}

function mantenerFocoEnModal(event) {
  const elementos = [...event.currentTarget.querySelectorAll(
    'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
  )].filter(elemento => elemento.offsetParent !== null)
  const primero = elementos[0]
  const ultimo = elementos[elementos.length - 1]

  if (event.shiftKey && document.activeElement === primero) {
    event.preventDefault()
    ultimo?.focus()
  } else if (!event.shiftKey && document.activeElement === ultimo) {
    event.preventDefault()
    primero?.focus()
  }
}
</script>

<template>
  <section class="contracts-page">
    <header class="intro">
      <div>
        <span class="eyebrow"><FileText :size="16" /> CONTRATOS</span>
        <h1>Contratos y seguimiento</h1>
        <p>Consulta los contratos y revisa la información disponible sobre su ejecución y nivel de riesgo.</p>
      </div>
      <div class="summary" aria-label="Resumen de contratos">
        <div>
          <b>{{ contratos.length }}</b>
          <span>contratos</span>
        </div>
        <div class="high">
          <b>{{ totalPorRiesgo('alto') }}</b>
          <span>riesgo alto</span>
        </div>
        <div class="medium">
          <b>{{ totalPorRiesgo('medio') }}</b>
          <span>riesgo medio</span>
        </div>
      </div>
    </header>

    <aside class="demo-note">
      <ShieldAlert :size="18" />
      <p><strong>Datos de demostración.</strong> Los contratos, entidades, valores y documentos mostrados son ficticios. El nivel de riesgo es ilustrativo y no constituye una conclusión sobre contratos reales.</p>
    </aside>

    <section class="card panel">
      <div class="toolbar">
        <label class="search">
          <Search :size="18" />
          <input v-model="busqueda" type="search" placeholder="Buscar ID, entidad, objeto o comuna" aria-label="Buscar contratos" />
        </label>

        <label class="select-filter">
          <span>Riesgo</span>
          <select v-model="riesgo" aria-label="Filtrar por riesgo">
            <option value="todos">Todos</option>
            <option value="alto">Alto</option>
            <option value="medio">Medio</option>
            <option value="bajo">Bajo</option>
          </select>
        </label>

        <label class="select-filter">
          <span>Estado</span>
          <select v-model="estado" aria-label="Filtrar por estado">
            <option value="todos">Todos</option>
            <option v-for="item in opcionesEstado.filter(v => v !== 'todos')" :key="item" :value="item">{{ item }}</option>
          </select>
        </label>

        <span class="result-count">{{ visibles.length }} resultados</span>
      </div>

      <div v-if="visibles.length" class="grid-list">
        <article v-for="item in visibles" :key="item.id" class="contract-card" :class="item.riesgo">
          <div class="topline">
            <span class="risk-pill" :class="item.riesgo">{{ item.riesgo }}</span>
            <span class="state-pill">{{ item.estado }}</span>
          </div>
          <h2>{{ item.objeto }}</h2>
          <p class="entity">{{ item.entidad }}</p>
          <dl>
            <div>
              <dt>ID</dt>
              <dd>{{ item.id }}</dd>
            </div>
            <div>
              <dt>Comuna</dt>
              <dd>{{ item.comuna }}</dd>
            </div>
            <div class="value-field">
              <dt>Valor</dt>
              <dd>{{ item.valor }}</dd>
            </div>
          </dl>
          <p class="description">{{ item.descripcion }}</p>
          <button class="details-button" @click="abrirContrato(item)">
            Ver contrato
            <ArrowRight :size="16" />
          </button>
        </article>
      </div>

      <div v-else class="empty">
        <ShieldAlert :size="28" />
        <h2>No encontramos contratos</h2>
        <p>Pruebe con otro término o cambie los filtros seleccionados.</p>
      </div>
    </section>

    <div v-if="contratoActivo" class="modal-backdrop" @click.self="cerrarContrato">
      <aside class="modal" role="dialog" aria-modal="true" aria-labelledby="contrato-title" @keydown.esc.window="cerrarContrato" @keydown.tab="mantenerFocoEnModal">
        <button ref="botonCerrar" class="close-button" type="button" aria-label="Cerrar ventana de contrato" @click="cerrarContrato">
          <X :size="18" />
        </button>

        <div class="modal-header">
          <div>
            <span class="eyebrow dark"><FileText :size="15" /> {{ contratoActivo.id }}</span>
            <h2 id="contrato-title">{{ contratoActivo.objeto }}</h2>
          </div>
          <span class="risk-pill large" :class="contratoActivo.riesgo">{{ contratoActivo.riesgo }}</span>
        </div>

        <div class="modal-grid">
          <div class="info-block">
            <h3>Información general</h3>
            <ul>
              <li><strong>Entidad:</strong> {{ contratoActivo.entidad }}</li>
              <li><strong>Contratista:</strong> {{ contratoActivo.contratista }}</li>
              <li><strong>Comuna:</strong> {{ contratoActivo.comuna }}</li>
              <li><strong>Tipo:</strong> {{ contratoActivo.tipo }}</li>
              <li><strong>Fecha:</strong> {{ contratoActivo.fecha }}</li>
              <li><strong>Valor:</strong> {{ contratoActivo.valor }}</li>
              <li><strong>Estado:</strong> {{ contratoActivo.estado }}</li>
            </ul>
          </div>

          <div class="info-block accent">
            <h3>Resumen del caso</h3>
            <p>{{ contratoActivo.descripcion }}</p>
            <strong>Qué revisar</strong>
            <p>{{ contratoActivo.detalle }}</p>
          </div>
        </div>

        <div class="documents">
          <h3>Documentación sugerida para revisión</h3>
          <ul>
            <li v-for="doc in contratoActivo.documentos" :key="doc">{{ doc }}</li>
          </ul>
          <p>Estos nombres son ejemplos; no son enlaces ni archivos oficiales.</p>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.contracts-page { padding-top: 36px; padding-bottom: 32px; }
.intro { display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; margin-bottom: 24px; }
.eyebrow { display: inline-flex; align-items: center; gap: 8px; color: var(--red); font-size: 12px; letter-spacing: .1em; font-weight: 700; text-transform: uppercase; }
.eyebrow.dark { color: var(--navy); }
h1 { margin: 10px 0 8px; font-size: 32px; font-weight: 600; color: var(--ink); }
.intro p { max-width: 680px; margin: 0; color: var(--muted); line-height: 1.6; }
.demo-note { display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; margin-bottom: 20px; border: 1px solid #f2d9ae; border-radius: 10px; background: #fff9ed; color: #8a5300; }
.demo-note svg { flex: none; margin-top: 2px; }
.demo-note p { margin: 0; font-size: 13px; line-height: 1.55; }
.summary { display: flex; gap: 12px; }
.summary div { min-width: 118px; padding: 14px 18px; border: 1px solid var(--line); border-radius: 10px; background: #fff; }
.summary b, .summary span { display: block; }
.summary b { font-size: 24px; color: var(--ink); }
.summary span { margin-top: 3px; font-size: 12px; color: var(--muted); }
.summary .high b { color: var(--red); }
.summary .medium b { color: #a96300; }
.panel { overflow: hidden; }
.toolbar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 16px 20px; border-bottom: 1px solid var(--line); }
.search { display: flex; align-items: center; gap: 9px; flex: 1 1 270px; max-width: 420px; padding: 0 12px; border: 1px solid var(--line); border-radius: 8px; color: var(--muted); }
.search input { width: 100%; height: 40px; border: 0; outline: 0; background: transparent; color: var(--ink); font: inherit; font-size: 14px; }
.select-filter { display: flex; align-items: center; gap: 8px; padding: 0 10px; border: 1px solid var(--line); border-radius: 8px; color: var(--muted); font-size: 13px; }
.select-filter select { height: 40px; border: 0; background: transparent; color: var(--ink); font: inherit; font-weight: 600; }
.result-count { margin-left: auto; color: var(--muted); font-size: 13px; white-space: nowrap; }
.grid-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; padding: 20px; }
.contract-card { display: flex; flex-direction: column; gap: 16px; padding: 18px; border: 1px solid var(--line); border-radius: 12px; background: #fff; transition: transform .15s ease, box-shadow .15s ease; }
.contract-card:hover { transform: translateY(-1px); box-shadow: 0 8px 22px rgba(11, 42, 74, 0.06); }
.contract-card.alto { border-top: 4px solid var(--red); }
.contract-card.medio { border-top: 4px solid var(--amber); }
.contract-card.bajo { border-top: 4px solid var(--green); }
.topline { display: flex; justify-content: space-between; gap: 8px; }
.risk-pill { display: inline-flex; align-items: center; justify-content: center; min-width: 76px; height: 28px; padding: 0 10px; border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
.risk-pill.alto { background: var(--red-bg); color: var(--red); }
.risk-pill.medio { background: var(--amber-bg); color: #a96300; }
.risk-pill.bajo { background: var(--green-bg); color: var(--green); }
.risk-pill.large { min-width: 90px; }
.state-pill { display: inline-flex; align-items: center; justify-content: center; padding: 0 10px; border-radius: 999px; background: #eef4fb; color: var(--navy); font-size: 11px; font-weight: 600; }
.contract-card h2 { margin: 0; font-size: 20px; line-height: 1.4; color: var(--ink); }
.entity { margin: 0; color: var(--muted); font-size: 14px; }
.contract-card dl { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; margin: 0; }
.contract-card dl div { min-width: 0; }
.contract-card dl .value-field { grid-column: 1 / -1; }
.contract-card dt { font-size: 11px; letter-spacing: .06em; color: var(--muted); text-transform: uppercase; }
.contract-card dd { margin: 6px 0 0; font-weight: 600; color: var(--ink); overflow-wrap: anywhere; }
.description { margin: 0; font-size: 14px; color: var(--muted); line-height: 1.6; }
.details-button { display: inline-flex; align-items: center; justify-content: center; gap: 8px; margin-top: auto; border: 0; border-radius: 8px; background: var(--navy); color: #fff; padding: 10px 14px; font-weight: 600; }
.empty { display: grid; place-items: center; text-align: center; gap: 10px; padding: 42px 20px; color: var(--muted); }
.empty h2 { margin: 0; color: var(--ink); }
.empty p { margin: 0; }
.modal-backdrop { position: fixed; inset: 0; display: grid; place-items: center; padding: 24px; background: rgba(11, 42, 74, 0.4); z-index: 30; }
.modal { position: relative; width: min(760px, 100%); max-height: min(90vh, 820px); overflow: auto; background: #fff; border: 1px solid var(--line); border-radius: 18px; padding: 28px; box-shadow: 0 24px 70px rgba(13, 34, 61, 0.2); }
.close-button { position: absolute; top: 16px; right: 16px; display: grid; place-items: center; width: 36px; height: 36px; border: 0; border-radius: 50%; background: #edf2f8; color: var(--ink); }
.modal-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; padding-right: 32px; }
.modal-header h2 { margin: 10px 0 0; font-size: 26px; line-height: 1.3; color: var(--ink); }
.modal-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 18px; margin-top: 24px; }
.info-block { padding: 18px; border: 1px solid var(--line); border-radius: 12px; background: #f7f9fc; }
.info-block.accent { background: linear-gradient(180deg, #fff8f3 0%, #fff 100%); }
.info-block h3 { margin: 0 0 12px; font-size: 14px; letter-spacing: .08em; color: var(--muted); text-transform: uppercase; }
.info-block ul { margin: 0; padding-left: 18px; color: var(--ink); line-height: 1.9; }
.info-block p { margin: 8px 0 0; color: var(--muted); line-height: 1.7; }
.info-block strong { color: var(--ink); }
.documents { margin-top: 22px; padding-top: 14px; border-top: 1px solid var(--line); }
.documents h3 { margin: 0 0 12px; font-size: 14px; letter-spacing: .08em; color: var(--muted); text-transform: uppercase; }
.documents ul { margin: 0; padding-left: 18px; color: var(--ink); line-height: 1.9; }
.documents p { margin: 8px 0 0; color: var(--muted); font-size: 12px; }
@media (max-width: 760px) {
  .intro { flex-direction: column; align-items: flex-start; }
  .summary { width: 100%; flex-wrap: wrap; }
  .summary div { flex: 1 1 100px; min-width: 0; }
  .toolbar { padding: 14px; }
  .grid-list { grid-template-columns: 1fr; padding: 14px; }
  .modal-grid { grid-template-columns: 1fr; }
  .modal-header { padding-right: 0; }
  .modal { padding: 22px 18px; }
}
</style>
