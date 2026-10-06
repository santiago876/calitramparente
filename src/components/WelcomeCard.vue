<script setup>
import { ArrowRight, TriangleAlert, Map, CircleCheck } from 'lucide-vue-next'
const emit = defineEmits(['explorar', 'banderas'])
const items = [
  { icon: Map, color: 'var(--navy)', t: 'Explore el mapa', d: 'Haga clic en cualquier zona de Cali para ver qué proyectos hay en su barrio y cuánto dinero se ha invertido.' },
  { icon: TriangleAlert, color: 'var(--red)', t: 'Detecte anomalías', d: 'La sección Banderas Rojas muestra contratos con alertas: adiciones excesivas, prórrogas o contratación directa sospechosa.' },
  { icon: CircleCheck, color: 'var(--green)', t: 'Reporte y comparta', d: 'Cada contrato puede ser reportado a la veeduría ciudadana o descargado para investigaciones periodísticas.' },
]
</script>

<template>
  <section class="card welcome">
    <div class="bar"></div>
    <div class="body">
      <span class="pill"><i></i>Plataforma de Veeduría Ciudadana · Santiago de Cali</span>
      <h1>Bienvenido a CaliTransparente</h1>
      <p class="lead">Aquí puede consultar, en lenguaje sencillo, cómo se invierte el presupuesto público de Cali: qué contratos hay en su comuna, quiénes son los contratistas y si existen irregularidades.</p>
      <div class="grid">
        <div v-for="i in items" :key="i.t" class="item">
          <span class="ico" :style="{ color: i.color }"><component :is="i.icon" :size="22" /></span>
          <div><h3>{{ i.t }}</h3><p>{{ i.d }}</p></div>
        </div>
      </div>
      <div class="actions">
        <button class="primary" @click="emit('explorar')"><ArrowRight :size="18" /> Explorar el mapa</button>
        <button class="alert" @click="emit('banderas')"><TriangleAlert :size="18" /> Ver banderas rojas</button>
        <span class="src">Datos: SECOP II · Alcaldía de Cali · 2026</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.welcome{overflow:hidden;margin-top:24px}
.bar{height:6px;background:linear-gradient(90deg,var(--navy),var(--green) 60%,var(--red))}
.body{padding:30px}
.pill{display:inline-flex;align-items:center;gap:8px;background:#f1f4f8;border-radius:99px;padding:8px 16px;font-size:13px;font-weight:600}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--navy)}
h1{font-size:30px;font-weight:500;margin:20px 0 12px}
.lead{max-width:660px;color:var(--muted);line-height:1.65;margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.item{display:flex;gap:16px;padding:20px;border:1px solid var(--line);border-radius:12px;background:#fafbfd}
.ico{width:42px;height:42px;flex:none;display:grid;place-items:center;background:#fff;border:1px solid var(--line);border-radius:10px}
h3{margin:0 0 6px;font-size:16px;font-weight:500}
.item p{margin:0;color:var(--muted);font-size:14px;line-height:1.6}
.actions{display:flex;flex-wrap:wrap;align-items:center;gap:16px;margin-top:28px}
.actions button{display:flex;gap:10px;align-items:center;padding:14px 24px;border-radius:8px;font-weight:600}
.primary{background:var(--navy);color:#fff;border:0}
.alert{background:var(--red-bg);color:var(--red);border:1px solid #f5c2c0}
.src{margin-left:auto;font-size:13px;color:#98a4b5}
</style>
