<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const numQuestions = ref(50)

function startExam() {
  router.push({ name: 'exam-session', query: { count: numQuestions.value } })
}
</script>

<template>
  <div class="space-y-4">
    <div class="bg-white p-4 rounded shadow">
      <label class="block text-sm font-medium mb-1">试卷题目数量</label>
      <input v-model.number="numQuestions" type="number" min="1" class="w-40 rounded border p-2" />
    </div>
    <button class="bg-blue-600 text-white rounded px-4 py-2" @click="startExam">开始模拟考试</button>
  </div>
</template>
