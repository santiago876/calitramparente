<script setup>
import { computed, ref } from 'vue'
import { zonas } from '../data/comunas'

const filtro = defineModel('filtro', { default: 'todas' })
const filtros = [['todas', 'Todas las zonas'], ['alto', 'Riesgo Alto'], ['medio', 'Riesgo Medio'], ['bajo', 'Riesgo Bajo']]
const seleccion = ref(zonas.find(z => z.id === 'Corregimiento Sur'))
const visible = z => filtro.value === 'todas' || z.riesgo === filtro.value
const total = computed(() => zonas.filter(visible).length)
const badge = z => (z.riesgo === 'bajo' && !z.alertas ? '' : z.alertas)
const estado = z => (z.alertas ? (z.riesgo === 'alto' ? 'Alertas altas' : 'Alertas') : 'Sin alertas graves')
</script>

<template>
  <section>
    <div class="card filters">
      <span class="lbl">Filtrar por riesgo:</span>
      <button v-for="[id, t] in filtros" :key="id" :class="{ on: filtro === id }" @click="filtro = id">{{ t }}</button>
      <span class="count">{{ total }} zonas visibles</span>
    </div>

    <div class="layout">
      <div class="card map">
        <header>
          <div><h2>Santiago de Cali · 22 Comunas</h2><p>Haga clic en una zona para ver el detalle de inversión</p></div>
          <ul class="legend">
            <li><i class="g"></i>Sin alertas</li><li><i class="a"></i>Alerta media</li><li><i class="r"></i>Alerta alta</li>
          </ul>
        </header>
        <div class="grid-wrap">
          <div class="grid">
            <span class="north">N</span>
            <button v-for="z in zonas" :key="z.id" :class="[z.riesgo, { dim: !visible(z), sel: seleccion?.id === z.id }]"
                    :aria-label="`${z.nombre}, ${z.alertas} alertas`" @click="seleccion = z">
              <span v-if="badge(z) !== ''" class="badge">{{ badge(z) }}</span>
              <span v-if="z.riesgo !== 'bajo'" class="dot"></span>
              {{ z.nombre.length > 4 ? z.nombre.split(' ').map(w => w[0]).join('') : z.nombre }}
            </button>
          </div>
        </div>
      </div>

      <aside v-if="seleccion" class="card panel" :class="seleccion.riesgo">
        <div class="head">
          <div>
            <small>PERFIL DE INVERSIÓN</small>
            <h2>{{ seleccion.nombre }}</h2>
            <p>{{ seleccion.tipo ?? 'Comuna' }}</p>
          </div>
          <span class="state" :class="seleccion.riesgo">{{ estado(seleccion) }}</span>
        </div>
        <div class="kpis">
          <div><b>{{ seleccion.contratos ?? '—' }}</b><span>Contratos</span></div>
          <div><b>{{ seleccion.invertido ?? '—' }}</b><span>Invertido</span></div>
          <div :class="seleccion.riesgo"><b>{{ seleccion.alertas }}</b><span>Alertas</span></div>
        </div>
        <template v-if="seleccion.secretarias">
          <h4>SECRETARÍAS ACTIVAS</h4>
          <span v-for="s in seleccion.secretarias" :key="s" class="chip">{{ s }}</span>
          <h4>PROYECTOS DESTACADOS</h4>
          <ul class="proj"><li v-for="p in seleccion.proyectos" :key="p">{{ p }}</li></ul>
        </template>
        <p v-else class="empty">Aún no hay detalle de contratos para esta zona. Conecte la API para cargarlo.</p>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.filters{display:flex;align-items:center;gap:8px;padding:12px 20px;margin-top:24px;flex-wrap:wrap}
.lbl{font-size:14px;color:var(--muted);margin-right:8px}
.filters button{border:0;background:none;padding:9px 16px;border-radius:7px;font-weight:600;font-size:14px;color:var(--ink)}
.filters button.on{background:var(--navy);color:#fff}
.count{margin-left:auto;color:#a5b0bf;font-size:14px}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 375px;gap:24px;margin-top:24px;align-items:start}
.map header{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:22px 24px;border-bottom:1px solid var(--line)}
h2{margin:0;font-size:20px;font-weight:500}.map p,.panel p{margin:4px 0 0;color:var(--muted);font-size:14px}
.legend{display:flex;gap:18px;list-style:none;margin:0;padding:0;font-size:14px;color:var(--muted)}
.legend li{display:flex;align-items:center;gap:6px}
.legend i{width:14px;height:14px;border-radius:4px;border:2px solid}
.g{border-color:var(--green)}.a{border-color:var(--amber)}.r{border-color:var(--red)}
.grid-wrap{padding:28px;display:grid;place-items:center}
.grid{position:relative;display:grid;grid-template-columns:repeat(5,120px);gap:8px;padding:30px;background:#eef3fb;border-radius:20px}
.grid>button{position:relative;height:88px;border-radius:8px;border:1.5px solid #bfe3d0;background:var(--green-bg);color:#0b5c3b;font-weight:700;font-size:20px;transition:opacity .15s}
.grid>button.medio{background:var(--amber-bg);border-color:#f2d9ae;color:#9a5b05}
.grid>button.alto{background:var(--red-bg);border-color:#f4c1bf;color:#a31d1d}
.grid>button.dim{opacity:.25}
.grid>button.sel{outline:3px solid var(--green);outline-offset:-1px}
.badge{position:absolute;top:-8px;left:-8px;min-width:24px;height:24px;border-radius:50%;background:#d62828;color:#fff;font-size:12px;display:grid;place-items:center}
.dot{position:absolute;top:8px;right:8px;width:14px;height:14px;border-radius:50%;background:var(--amber)}
.alto .dot{background:var(--red)}
.north{position:absolute;top:-4px;right:-4px;z-index:1;width:38px;height:38px;border-radius:50%;background:#fff;border:1px solid var(--line);display:grid;place-items:center;font-weight:700}
.panel{border-top:5px solid var(--green);overflow:hidden}.panel.medio{border-top-color:var(--amber)}.panel.alto{border-top-color:var(--red)}
.head{display:flex;justify-content:space-between;gap:12px;padding:22px 24px;border-bottom:1px solid var(--line)}
small{font-size:11px;letter-spacing:.12em;color:var(--muted);font-weight:600}
.state{height:fit-content;font-size:12px;font-weight:600;padding:6px 12px;border-radius:99px;background:var(--green-bg);color:var(--green)}
.state.medio{background:var(--amber-bg);color:#9a5b05}.state.alto{background:var(--red-bg);color:var(--red)}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:24px 24px 4px}
.kpis div{background:#f4f6f9;border:1px solid var(--line);border-radius:10px;padding:14px 6px;text-align:center}
.kpis div.bajo{background:var(--green-bg)}.kpis div.alto{background:var(--red-bg)}.kpis div.medio{background:var(--amber-bg)}
.kpis b{display:block;font-size:22px;font-weight:400}.kpis span{font-size:12px;color:var(--muted)}
h4{margin:22px 24px 10px;font-size:12px;letter-spacing:.1em;color:var(--muted)}
.chip{display:inline-block;margin-left:24px;background:#e8f0fb;color:var(--navy);padding:6px 12px;border-radius:99px;font-size:13px;font-weight:500}
.proj{margin:0 24px 24px;padding:0;list-style:none}.proj li{display:flex;gap:10px;align-items:center;font-size:14px}
.proj li::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--green)}
.empty{padding:24px}
@media(max-width:1100px){.layout{grid-template-columns:1fr}.grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:600px){.grid{padding:20px 12px}.grid-wrap{padding:12px}.grid>button{height:64px;font-size:15px}}
</style>
