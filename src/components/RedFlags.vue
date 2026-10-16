<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { Search, TriangleAlert, ChevronDown, ChevronUp, SlidersHorizontal } from 'lucide-vue-next'
import { obtenerBanderasRojas, usaDatosDemo } from '../services/redFlags'

const banderas = ref([])
const busqueda = ref('')
const riesgo = ref('todos')
const tipo = ref('todos')
const expandida = ref(null)
const cargando = ref(true)
const error = ref('')
const controller = new AbortController()

const tipos = computed(() => [...new Set(banderas.value.map(b => b.tipo))])
const visibles = computed(() => banderas.value.filter(b => {
  const texto = `${b.id} ${b.entidad} ${b.objeto} ${b.contratista} ${b.tipo}`.toLocaleLowerCase()
  return (riesgo.value === 'todos' || b.riesgo === riesgo.value)
    && (tipo.value === 'todos' || b.tipo === tipo.value)
    && texto.includes(busqueda.value.trim().toLocaleLowerCase())
}))

const conteo = nivel => banderas.value.filter(b => b.riesgo === nivel).length
const severidad = nivel => ({ alto: 'Riesgo alto', medio: 'Riesgo medio', bajo: 'Riesgo bajo' })[nivel]

async function cargarBanderas() {
  cargando.value = true
  error.value = ''

  try {
    banderas.value = await obtenerBanderasRojas({ signal: controller.signal })
  } catch (err) {
    if (err.name !== 'AbortError') {
      error.value = err.message || 'Ocurrió un error inesperado al cargar las alertas.'
    }
  } finally {
    cargando.value = false
  }
}

onMounted(cargarBanderas)
onUnmounted(() => controller.abort())
</script>

<template>
  <section class="flags-page">
    <section class="intro">
      <div>
        <span class="eyebrow"><TriangleAlert :size="16" /> VEEDURÍA CIUDADANA</span>
        <h1>Banderas rojas</h1>
        <p>Señales que ayudan a identificar contratos que podrían requerir una revisión más detallada.</p>
      </div>
      <div class="summary" aria-label="Resumen de alertas">
        <div><b>{{ banderas.length }}</b><span>señales registradas</span></div>
        <div class="high"><b>{{ conteo('alto') }}</b><span>riesgo alto</span></div>
        <div class="medium"><b>{{ conteo('medio') }}</b><span>riesgo medio</span></div>
      </div>
    </section>

    <aside v-if="usaDatosDemo" class="demo-note">
      <TriangleAlert :size="18" />
      <p><strong>Datos de demostración.</strong> Estos contratos y alertas son ficticios y solo ilustran la interfaz. Una bandera roja es una señal de revisión, no una prueba de corrupción o ilegalidad.</p>
    </aside>

    <section class="card results">
      <div class="toolbar">
        <label class="search">
          <Search :size="18" />
          <input v-model="busqueda" type="search" placeholder="Buscar contrato, entidad o contratista" aria-label="Buscar alertas" />
        </label>
        <label class="select-filter">
          <SlidersHorizontal :size="16" />
          <span>Riesgo</span>
          <select v-model="riesgo" aria-label="Filtrar por nivel de riesgo">
            <option value="todos">Todos</option>
            <option value="alto">Alto</option>
            <option value="medio">Medio</option>
            <option value="bajo">Bajo</option>
          </select>
        </label>
        <label class="select-filter">
          <span>Tipo de alerta</span>
          <select v-model="tipo" aria-label="Filtrar por tipo de alerta">
            <option value="todos">Todos los tipos</option>
            <option v-for="item in tipos" :key="item" :value="item">{{ item }}</option>
          </select>
        </label>
        <span class="result-count">{{ visibles.length }} de {{ banderas.length }} señales</span>
      </div>

      <div v-if="cargando" class="empty" role="status">
        <p>Cargando banderas rojas…</p>
      </div>
      <div v-else-if="error" class="load-error" role="alert">
        <TriangleAlert :size="22" />
        <div><strong>No se pudieron cargar las banderas rojas.</strong><p>{{ error }}</p></div>
        <button @click="cargarBanderas">Reintentar</button>
      </div>
      <div v-else-if="visibles.length" class="alert-list">
        <article v-for="item in visibles" :key="item.id" class="alert-row" :class="item.riesgo">
          <div class="alert-icon"><TriangleAlert :size="20" /></div>
          <div class="alert-content">
            <div class="row-heading">
              <span class="risk-pill" :class="item.riesgo">{{ severidad(item.riesgo) }}</span>
              <span class="kind">{{ item.tipo }}</span>
              <span class="demo-id">{{ item.id }}</span>
            </div>
            <h2>{{ item.objeto }}</h2>
            <p class="entity">{{ item.entidad }} <span>·</span> {{ item.contratista }}</p>
            <p class="description">{{ item.descripcion }}</p>
            <div class="meta"><strong>{{ item.valor }}</strong><span>Fecha de referencia: {{ item.fecha }}</span></div>
            <div v-if="expandida === item.id" class="detail" role="region">
              <strong>Qué revisar</strong>
              <p>{{ item.detalle }}</p>
              <small>Identificador ilustrativo · {{ item.id }}</small>
            </div>
          </div>
          <button class="details-button" :aria-expanded="expandida === item.id" @click="expandida = expandida === item.id ? null : item.id">
            {{ expandida === item.id ? 'Ocultar' : 'Ver detalle' }}
            <ChevronUp v-if="expandida === item.id" :size="16" />
            <ChevronDown v-else :size="16" />
          </button>
        </article>
      </div>
      <div v-else class="empty">
        <Search :size="28" />
        <h2>No encontramos alertas</h2>
        <p>Pruebe con otro término o cambie los filtros seleccionados.</p>
        <button @click="busqueda = ''; riesgo = 'todos'; tipo = 'todos'">Limpiar filtros</button>
      </div>
    </section>
    <p class="source-note">{{ usaDatosDemo ? 'Los ejemplos son ficticios y deben reemplazarse conectando el backend.' : 'Cada señal debe contrastarse con los documentos oficiales publicados en SECOP II.' }}</p>
  </section>
</template>

<style scoped>
.flags-page{padding-top:36px;padding-bottom:8px}
.intro{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:24px}
.eyebrow{display:flex;align-items:center;gap:8px;color:var(--red);font-size:12px;font-weight:700;letter-spacing:.1em}
h1{margin:10px 0 8px;font-size:32px;font-weight:600;color:var(--ink)}
.intro p{max-width:650px;margin:0;color:var(--muted);line-height:1.6}
.summary{display:flex;gap:12px}
.summary div{min-width:118px;padding:14px 18px;border:1px solid var(--line);border-radius:10px;background:#fff}
.summary b,.summary span{display:block}
.summary b{font-size:24px;color:var(--ink)}
.summary span{margin-top:3px;font-size:12px;color:var(--muted)}
.summary .high b{color:var(--red)}.summary .medium b{color:#a96300}
.demo-note{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;margin-bottom:20px;border:1px solid #f2d9ae;border-radius:10px;background:#fff9ed;color:#8a5300}
.demo-note svg{flex:none;margin-top:2px}
.demo-note p{margin:0;font-size:13px;line-height:1.55}
.results{overflow:hidden}
.toolbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:16px 20px;border-bottom:1px solid var(--line)}
.search{display:flex;align-items:center;gap:9px;flex:1 1 270px;max-width:440px;padding:0 12px;border:1px solid var(--line);border-radius:8px;color:var(--muted)}
.search input{width:100%;height:40px;border:0;outline:0;background:transparent;color:var(--ink);font:inherit;font-size:14px}
.select-filter{display:flex;align-items:center;gap:8px;padding:0 10px;border:1px solid var(--line);border-radius:8px;color:var(--muted);font-size:13px}
.select-filter select{height:40px;border:0;background:transparent;color:var(--ink);font:inherit;font-weight:600}
.result-count{margin-left:auto;color:var(--muted);font-size:13px;white-space:nowrap}
.load-error{display:flex;align-items:center;gap:14px;padding:24px;color:var(--red)}
.load-error div{flex:1}
.load-error strong{font-size:14px}
.load-error p{margin:4px 0 0;color:var(--muted);font-size:13px;overflow-wrap:anywhere}
.load-error button{padding:9px 14px;border:0;border-radius:7px;background:var(--navy);color:#fff;font-weight:600}
.alert-list{display:grid}
.alert-row{display:flex;align-items:flex-start;gap:16px;padding:22px 20px;border-bottom:1px solid var(--line)}
.alert-row:last-child{border-bottom:0}
.alert-icon{display:grid;place-items:center;flex:none;width:42px;height:42px;border-radius:10px;background:var(--red-bg);color:var(--red)}
.alert-row.medio .alert-icon{background:var(--amber-bg);color:#a96300}
.alert-row.bajo .alert-icon{background:var(--green-bg);color:var(--green)}
.alert-content{flex:1;min-width:0}
.row-heading{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.risk-pill{padding:4px 9px;border-radius:99px;background:var(--red-bg);color:var(--red);font-size:11px;font-weight:700}
.risk-pill.medio{background:var(--amber-bg);color:#925800}
.risk-pill.bajo{background:var(--green-bg);color:var(--green)}
.kind{font-size:12px;font-weight:600;color:var(--muted)}
.demo-id{margin-left:auto;color:#9aa6b5;font:11px ui-monospace,Menlo,monospace}
.alert-content h2{margin:9px 0 3px;font-size:17px;font-weight:600}
.entity,.description{margin:0;font-size:13px;line-height:1.5}
.entity{color:var(--muted)}.entity span{padding:0 3px}
.description{margin-top:8px;color:var(--ink)}
.meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--muted)}
.meta strong{color:var(--ink)}
.details-button{display:flex;align-items:center;gap:6px;flex:none;padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--navy);font-size:12px;font-weight:600}
.detail{margin-top:14px;padding:14px 16px;border-left:3px solid var(--red);border-radius:0 8px 8px 0;background:#f8fafc}
.alert-row.medio .detail{border-left-color:var(--amber)}.alert-row.bajo .detail{border-left-color:var(--green)}
.detail strong{font-size:12px}.detail p{margin:5px 0 8px;color:var(--muted);font-size:13px;line-height:1.55}.detail small{color:#9aa6b5;font-size:11px}
.empty{display:grid;justify-items:center;padding:56px 20px;text-align:center;color:var(--muted)}
.empty h2{margin:12px 0 4px;color:var(--ink);font-size:18px}.empty p{margin:0 0 16px;font-size:14px}
.empty button{padding:9px 14px;border:0;border-radius:7px;background:var(--navy);color:#fff;font-weight:600}
.source-note{margin:14px 2px 0;color:#8895a6;font-size:12px;line-height:1.5}
@media(max-width:760px){.intro{align-items:flex-start;flex-direction:column}.summary{width:100%}.summary div{flex:1;min-width:0;padding:12px}.alert-row{gap:11px;padding:18px 14px}.alert-icon{width:36px;height:36px}.details-button{font-size:0;gap:0}.details-button svg{width:18px;height:18px}.result-count{margin-left:0}}
@media(max-width:480px){.flags-page{padding-top:24px}.summary{gap:7px}.summary span{font-size:11px}.alert-row{flex-wrap:wrap}.alert-content{flex-basis:calc(100% - 52px)}.details-button{margin-left:48px}.search{max-width:none}}
</style>
