<script setup>
import { Download } from 'lucide-vue-next'
defineProps({ vista: String })
const emit = defineEmits(['update:vista'])
const tabs = [['mapa', 'Mapa Interactivo'], ['banderas', 'Banderas Rojas'], ['contratos', 'Contratos']]
</script>

<template>
  <header>
    <div class="top">
      <span>ALCALDÍA DE SANTIAGO DE CALI · VEEDURÍA CIUDADANA · DATOS ABIERTOS SECOP II</span>
      <span class="upd">Actualizado: Sep 10, 2026</span>
    </div>
    <div class="nav container">
      <div class="brand">
        <div class="logo">CT</div>
        <div><strong>CaliTransparente</strong><small>ANALÍTICA DE CONTRATACIÓN</small></div>
      </div>
      <nav>
        <button v-for="[id, label] in tabs" :key="id" :class="{ on: vista === id }" @click="emit('update:vista', id)">{{ label }}</button>
      </nav>
      <div class="right">
        <span class="status"><i></i>Sistema activo</span>
        <button class="report"><Download :size="16" /> Reportar</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
header{background:var(--navy);color:#fff}
.top{background:var(--navy-dark);display:flex;justify-content:space-between;padding:8px 24px;font:12px ui-monospace,Menlo,monospace;letter-spacing:.06em}
.upd{color:#7fe0b4}
.nav{display:flex;align-items:center;gap:32px;height:70px}
.brand{display:flex;gap:16px;align-items:center}
.logo{width:40px;height:45px;background:#fff;color:var(--navy);display:grid;place-items:center;font-weight:700;border-radius:4px}
.brand strong{display:block;font-size:19px;font-weight:500}
.brand small{font-size:11px;letter-spacing:.12em;color:#9db8d6}
nav{display:flex;gap:6px}
nav button{background:none;border:0;color:#fff;padding:10px 20px;border-radius:6px;font-weight:500}
nav button.on{background:rgba(255,255,255,.14)}
.right{margin-left:auto;display:flex;align-items:center;gap:20px}
.status{display:flex;align-items:center;gap:8px}
.status i{width:8px;height:8px;border-radius:50%;background:#2bb673}
.report{display:flex;gap:8px;align-items:center;background:var(--red);color:#fff;border:0;border-radius:6px;padding:10px 16px;font-weight:600}
@media(max-width:900px){.nav{flex-wrap:wrap;height:auto;padding:12px 24px;gap:12px}.top span:first-child{display:none}}
</style>
