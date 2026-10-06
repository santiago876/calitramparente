<script setup>
import { Wallet, CircleCheck, TriangleAlert } from 'lucide-vue-next'
import { resumen as r } from '../data/comunas'
</script>

<template>
  <div class="stats">
    <article class="blue">
      <span class="ico"><Wallet :size="22" /></span>
      <div><small>PRESUPUESTO TOTAL</small><b>{{ r.presupuesto }}</b><p>{{ r.contratos }} contratos · {{ r.secretarias }} secretarías</p></div>
    </article>
    <article class="card">
      <span class="ico g"><CircleCheck :size="22" /></span>
      <div>
        <small>CONTRATOS AUDITADOS</small>
        <b>{{ r.auditados }}<em>/{{ r.contratos }}</em></b>
        <div class="track"><div :style="{ width: r.cobertura + '%' }"></div></div>
        <p>{{ r.cobertura }}% de cobertura</p>
      </div>
    </article>
    <article class="card red">
      <span class="ico r"><TriangleAlert :size="22" /></span>
      <div><small>BANDERAS ROJAS</small><b>{{ r.banderas }}</b><p>anomalías detectadas · {{ r.adicionProm }}% adición prom.</p></div>
    </article>
  </div>
</template>

<style scoped>
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:24px}
article{display:flex;gap:20px;padding:24px;border-radius:14px}
.blue{background:var(--navy);color:#fff}
.card.red{border-color:#f5c2c0;background:#fffafa}
.ico{width:56px;height:56px;flex:none;display:grid;place-items:center;border-radius:12px;background:rgba(255,255,255,.12)}
.ico.g{background:#eaf3fb;color:var(--green)}.ico.r{background:var(--red-bg);color:var(--red)}
small{font-size:12px;font-weight:600;letter-spacing:.1em;color:#8fd8b4}
.card small{color:var(--muted)}.red small{color:var(--red)}
b{display:block;font-size:38px;font-weight:400;margin:4px 0}
.red b{color:var(--red)}
em{font-size:22px;font-style:normal;color:#98a4b5}
p{margin:0;font-size:14px;color:var(--muted)}.blue p{color:#cfe0f2}
.track{width:200px;height:6px;border-radius:9px;background:#e8edf3;margin:6px 0 10px}
.track div{height:100%;border-radius:9px;background:var(--green)}
</style>
