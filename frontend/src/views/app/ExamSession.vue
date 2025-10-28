<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getExamPaperApi, submitExamAnswerApi, finishExamApi } from '../../services/questions'
import type { ExamPaper, AnswerSubmission } from '../../types/questions'

const route = useRoute()
const count = Number(route.query.count || 50)

const paper = ref<ExamPaper | null>(null)
const currentIndex = ref(0)
const selectedOption = ref<number | null>(null)

const currentQuestion = computed(() => paper.value?.questions[currentIndex.value] || null)

async function loadPaper() {
  paper.value = await getExamPaperApi({ count })
  currentIndex.value = 0
  selectedOption.value = null
}

async function submitOne() {
  if (!currentQuestion.value || selectedOption.value === null) return
  const payload: AnswerSubmission = {
    question_id: currentQuestion.value.id,
    selected_option: selectedOption.value,
    paper_id: paper.value!.id,
  }
  await submitExamAnswerApi(payload)
}

async function nextQ() {
  if (currentIndex.value < (paper.value?.questions.length || 0) - 1) {
    currentIndex.value += 1
    selectedOption.value = null
  }
}

async function finish() {
  if (!paper.value) return
  await finishExamApi(paper.value.id)
}

onMounted(loadPaper)
</script>

<template>
  <div v-if="paper" class="space-y-4">
    <div class="bg-white p-4 rounded shadow">
      <div class="flex justify-between items-center">
        <h2 class="font-semibold">第 {{ currentIndex + 1 }} / {{ paper.questions.length }} 题</h2>
        <div class="text-sm text-gray-500">试卷编号：{{ paper.id }}</div>
      </div>
      <div v-if="currentQuestion" class="mt-2">
        <p class="font-medium">{{ currentQuestion.content }}</p>
        <ul class="mt-2 space-y-2">
          <li v-for="(opt, idx) in currentQuestion.options" :key="idx">
            <label class="flex items-center gap-2">
              <input type="radio" :value="idx" v-model="selectedOption" />
              <span>{{ opt }}</span>
            </label>
          </li>
        </ul>
      </div>
    </div>
    <div class="flex gap-2">
      <button class="bg-blue-600 text-white rounded px-4 py-2" @click="submitOne">提交本题</button>
      <button class="bg-gray-200 rounded px-4 py-2" @click="nextQ">下一题</button>
      <button class="bg-green-600 text-white rounded px-4 py-2" @click="finish">交卷</button>
    </div>
  </div>
</template>
