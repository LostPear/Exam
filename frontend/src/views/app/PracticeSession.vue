<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getPracticeQuestionApi, submitPracticeAnswerApi } from '../../services/questions'
import type { Question, AnswerSubmission } from '../../types/questions'

const route = useRoute()
const mode = (route.query.mode as 'sequential' | 'random') || 'random'

const question = ref<Question | null>(null)
const selectedOption = ref<number | null>(null)
const feedback = ref<string>('')

async function loadQuestion() {
  const q = await getPracticeQuestionApi({ mode })
  question.value = q
  selectedOption.value = null
  feedback.value = ''
}

async function submitAnswer() {
  if (!question.value || selectedOption.value === null) return
  const payload: AnswerSubmission = {
    question_id: question.value.id,
    selected_option: selectedOption.value,
  }
  const res = await submitPracticeAnswerApi(payload)
  feedback.value = res.correct ? '回答正确' : '回答错误'
}

onMounted(loadQuestion)
</script>

<template>
  <div class="space-y-4">
    <div class="bg-white shadow rounded p-4" v-if="question">
      <h2 class="font-semibold">{{ question.content }}</h2>
      <ul class="mt-2 space-y-2">
        <li v-for="(opt, idx) in question.options" :key="idx">
          <label class="flex items-center gap-2">
            <input type="radio" :value="idx" v-model="selectedOption" />
            <span>{{ opt }}</span>
          </label>
        </li>
      </ul>
    </div>
    <div class="flex gap-2">
      <button class="bg-blue-600 text-white rounded px-4 py-2" @click="submitAnswer">提交</button>
      <button class="bg-gray-200 rounded px-4 py-2" @click="loadQuestion">下一题</button>
    </div>
    <p v-if="feedback" :class="feedback==='回答正确' ? 'text-green-600' : 'text-red-600'">{{ feedback }}</p>
  </div>
</template>
