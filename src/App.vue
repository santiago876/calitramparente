<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import WelcomeCard from './components/WelcomeCard.vue'
import StatCards from './components/StatCards.vue'
import RiskMap from './components/RiskMap.vue'

const vista = ref('mapa')
const filtro = ref('todas')
const mapa = ref(null)
const explorar = () => mapa.value?.scrollIntoView({ behavior: 'smooth' })
const banderas = () => { filtro.value = 'alto'; explorar() }
</script>

<template>
  <AppHeader v-model:vista="vista" />
  <main class="container" style="padding-bottom:48px">
    <template v-if="vista === 'mapa'">
      <WelcomeCard @explorar="explorar" @banderas="banderas" />
      <StatCards />
      <div ref="mapa"><RiskMap v-model:filtro="filtro" /></div>
    </template>
    <p v-else style="margin-top:48px;color:var(--muted)">Vista en construcción.</p>
  </main>
</template>
