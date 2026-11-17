<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { AlertTriangle, CheckCircle2, X } from 'lucide-vue-next'
import { enviarReporte } from '../services/reports'

const emit = defineEmits(['close'])
const dialog = ref(null)
const form = ref(null)
const closeButton = ref(null)
const sending = ref(false)
const error = ref('')
const sent = ref(false)
const previousFocus = ref(null)

const report = ref({
  contractId: '',
  category: '',
  description: '',
  name: '',
  email: '',
})

const categories = [
  'Posible sobrecosto o adición',
  'Retrasos o prórrogas',
  'Posible incumplimiento',
  'Documentación incompleta',
  'Posible fraccionamiento',
  'Otro',
]

function close() {
  if (sending.value) return
  emit('close')
}

function onKeydown(event) {
  if (event.key === 'Escape') {
    close()
    return
  }

  if (event.key !== 'Tab' || !dialog.value) return
  const items = [...dialog.value.querySelectorAll(
    'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled])',
  )].filter(element => element.offsetParent !== null)
  const first = items[0]
  const last = items[items.length - 1]

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last?.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first?.focus()
  }
}

async function submitReport() {
  if (!form.value?.reportValidity() || sending.value) return
  sending.value = true
  error.value = ''

  const payload = {
    contract_id: report.value.contractId.trim() || null,
    category: report.value.category,
    description: report.value.description.trim(),
    reporter_name: report.value.name.trim() || null,
    reporter_email: report.value.email.trim() || null,
  }

  try {
    await enviarReporte(payload)
    sent.value = true
  } catch (err) {
    error.value = err.message || 'Ocurrió un error inesperado al enviar el reporte.'
  } finally {
    sending.value = false
  }
}

onMounted(async () => {
  previousFocus.value = document.activeElement
  document.addEventListener('keydown', onKeydown)
  await nextTick()
  closeButton.value?.focus()
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
  previousFocus.value?.focus()
})
</script>

<template>
  <div class="backdrop" @click.self="close">
    <section ref="dialog" class="dialog" role="dialog" aria-modal="true" aria-labelledby="report-title">
      <button ref="closeButton" class="close" type="button" aria-label="Cerrar formulario de reporte" :disabled="sending" @click="close">
        <X :size="19" />
      </button>

      <template v-if="sent">
        <div class="success-icon"><CheckCircle2 :size="30" /></div>
        <h2 id="report-title">Reporte enviado</h2>
        <p class="success-copy">El reporte fue recibido por el sistema. Gracias por ayudar a revisar la contratación pública.</p>
        <button class="primary" type="button" @click="close">Cerrar</button>
      </template>
      <template v-else>
        <span class="eyebrow"><AlertTriangle :size="16" /> VEEDURÍA CIUDADANA</span>
        <h2 id="report-title">Reportar una posible anomalía</h2>
        <p class="intro">Comparte información concreta sobre un contrato para que pueda revisarse. El envío no implica que exista una irregularidad comprobada.</p>

        <form ref="form" @submit.prevent="submitReport">
          <label>
            ID del contrato <span>Opcional</span>
            <input v-model="report.contractId" name="contractId" maxlength="100" placeholder="Ej. SECOP-II-12345" autocomplete="off" />
          </label>

          <label>
            Tipo de situación <span class="required">Requerido</span>
            <select v-model="report.category" name="category" required>
              <option value="" disabled>Seleccione una opción</option>
              <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
            </select>
          </label>

          <label>
            Descripción de lo observado <span class="required">Requerido</span>
            <textarea v-model="report.description" name="description" required minlength="20" maxlength="3000" rows="5"
              placeholder="Indique qué ocurrió, cuándo y qué documentos o hechos pueden ayudar a verificarlo."></textarea>
            <small>{{ report.description.length }}/3000 caracteres (mínimo 20)</small>
          </label>

          <div class="contact-grid">
            <label>
              Nombre <span>Opcional</span>
              <input v-model="report.name" name="name" maxlength="120" autocomplete="name" />
            </label>
            <label>
              Correo electrónico <span>Opcional</span>
              <input v-model="report.email" name="email" type="email" maxlength="254" autocomplete="email" />
            </label>
          </div>

          <p class="privacy">No incluyas datos personales sensibles ni información privada de terceros. Tus datos de contacto son opcionales.</p>

          <p v-if="error" class="error" role="alert">{{ error }}</p>
          <div class="actions">
            <button class="secondary" type="button" :disabled="sending" @click="close">Cancelar</button>
            <button class="primary" type="submit" :disabled="sending">{{ sending ? 'Enviando…' : 'Enviar reporte' }}</button>
          </div>
        </form>
      </template>
    </section>
  </div>
</template>

<style scoped>
.backdrop { position: fixed; inset: 0; z-index: 40; display: grid; place-items: center; padding: 20px; background: rgba(11, 42, 74, .52); }
.dialog { position: relative; width: min(620px, 100%); max-height: 92vh; overflow-y: auto; padding: 30px; border: 1px solid var(--line); border-radius: 16px; background: #fff; box-shadow: 0 24px 70px rgba(13, 34, 61, .24); }
.close { position: absolute; top: 16px; right: 16px; display: grid; place-items: center; width: 36px; height: 36px; border: 0; border-radius: 50%; background: #edf2f8; color: var(--ink); }
.eyebrow { display: inline-flex; align-items: center; gap: 7px; color: var(--red); font-size: 11px; font-weight: 700; letter-spacing: .1em; }
h2 { margin: 10px 40px 8px 0; color: var(--ink); font-size: 25px; line-height: 1.3; }
.intro, .success-copy { margin: 0 0 20px; color: var(--muted); font-size: 14px; line-height: 1.6; }
form { display: grid; gap: 16px; }
label { display: grid; gap: 7px; color: var(--ink); font-size: 13px; font-weight: 600; }
label span { display: inline; margin-left: 5px; color: var(--muted); font-size: 11px; font-weight: 400; }
label span.required { color: var(--red); }
input, select, textarea { width: 100%; padding: 11px 12px; border: 1px solid #cfd8e3; border-radius: 8px; background: #fff; color: var(--ink); font: inherit; font-size: 14px; }
textarea { resize: vertical; min-height: 110px; line-height: 1.5; }
label small { color: var(--muted); font-size: 11px; font-weight: 400; text-align: right; }
.contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.privacy { margin: -3px 0 0; color: var(--muted); font-size: 12px; line-height: 1.5; }
.error { margin: 0; padding: 11px 12px; border: 1px solid #f3c4c2; border-radius: 8px; background: #fff5f4; color: #a31d1d; font-size: 13px; line-height: 1.5; }
.actions { display: flex; justify-content: flex-end; gap: 10px; padding-top: 4px; }
.primary, .secondary { min-height: 42px; padding: 0 16px; border-radius: 8px; font: inherit; font-size: 14px; font-weight: 600; }
.primary { border: 0; background: var(--navy); color: #fff; }
.secondary { border: 1px solid var(--line); background: #fff; color: var(--ink); }
button:disabled { cursor: wait; opacity: .7; }
.success-icon { display: grid; place-items: center; width: 54px; height: 54px; margin-bottom: 12px; border-radius: 50%; background: var(--green-bg); color: var(--green); }
.success-copy { margin-bottom: 22px; }
@media (max-width: 560px) {
  .dialog { padding: 26px 18px 20px; }
  h2 { font-size: 22px; }
  .contact-grid { grid-template-columns: 1fr; }
}
</style>
