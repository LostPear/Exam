<script setup lang="ts">
import { ref } from 'vue'
import { importQuestionsApi } from '../../services/questions'

const file = ref<File | null>(null)
const message = ref('')

function onFile(e: Event) {
  const target = e.target as HTMLInputElement
  file.value = target.files?.[0] || null
}

async function onSubmit() {
  if (!file.value) return
  const form = new FormData()
  form.append('file', file.value)
  await importQuestionsApi(form)
  message.value = '导入成功'
}
</script>

<template>
  <div class="space-y-4 bg-white p-4 rounded shadow max-w-lg">
    <input type="file" accept=".csv,.xlsx,.json" @change="onFile" />
    <button class="bg-blue-600 text-white rounded px-4 py-2" @click="onSubmit">导入题库</button>
    <p v-if="message" class="text-green-600">{{ message }}</p>
  </div>
</template>
