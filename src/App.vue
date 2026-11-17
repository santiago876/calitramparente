<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import WelcomeCard from './components/WelcomeCard.vue'
import StatCards from './components/StatCards.vue'
import RiskMap from './components/RiskMap.vue'
import RedFlags from './components/RedFlags.vue'
import Contratos from './components/Contratos.vue'
import Informes from './components/Informes.vue'
import ReportForm from './components/ReportForm.vue'

const vista = ref('mapa')
const filtro = ref('todas')
const mapa = ref(null)
const mostrarReporte = ref(false)
const explorar = () => mapa.value?.scrollIntoView({ behavior: 'smooth' })
const banderas = () => { vista.value = 'banderas' }
</script>

<template>
  <AppHeader v-model:vista="vista" @report="mostrarReporte = true" />
  <ReportForm v-if="mostrarReporte" @close="mostrarReporte = false" />
  <main class="container" style="padding-bottom:48px">
    <template v-if="vista === 'mapa'">
      <WelcomeCard @explorar="explorar" @banderas="banderas" />
      <StatCards />
      <div ref="mapa"><RiskMap v-model:filtro="filtro" /></div>
    </template>
    <RedFlags v-else-if="vista === 'banderas'" />
    <Contratos v-else-if="vista === 'contratos'" />
    <Informes v-else-if="vista === 'informes'" />
    <p v-else style="margin:48px 0;color:var(--muted)">Vista en construcción.</p>
  </main>
</template>
