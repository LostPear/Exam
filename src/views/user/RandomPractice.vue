<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- 练习设置 -->
    <div v-if="!practicing" class="card">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">随机练习设置</h1>
      
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            练习题目数量
          </label>
          <select v-model="settings.count" class="input-field">
            <option :value="10">10 题</option>
            <option :value="20">20 题</option>
            <option :value="50">50 题</option>
            <option :value="100">100 题</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            题目类型
          </label>
          <div class="space-y-2">
            <label class="flex items-center">
              <input
                v-model="settings.types"
                type="checkbox"
                value="single"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-gray-700">单选题</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="settings.types"
                type="checkbox"
                value="judge"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-gray-700">判断题</span>
            </label>
          </div>
        </div>

        <button
          @click="startPractice"
          :disabled="settings.types.length === 0"
          class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          开始练习
        </button>
      </div>
    </div>

    <!-- 练习界面（复用 SequentialPractice 的逻辑） -->
    <template v-else>
      <!-- 顶部进度条 -->
      <div class="card">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-lg font-semibold text-gray-900">随机练习</h2>
          <span class="text-sm text-gray-600">题目 {{ currentIndex + 1 }} / {{ questions.length }}</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="bg-primary-600 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <!-- 题目卡片 -->
      <div v-if="currentQuestion" class="card">
        <div class="flex items-center justify-between mb-4">
          <span class="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">
            {{ currentQuestion.type }}
          </span>
        </div>

        <div class="mb-6">
          <h3 class="text-xl font-medium text-gray-900 mb-4">
            {{ currentQuestion.question }}
          </h3>
        </div>

        <div class="space-y-3">
          <div
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            @click="selectOption(index)"
            class="p-4 border-2 rounded-lg cursor-pointer transition-all"
            :class="getOptionClass(index)"
          >
            <div class="flex items-center">
              <div
                class="h-6 w-6 rounded-full border-2 flex items-center justify-center mr-3"
                :class="getOptionCircleClass(index)"
              >
                <div
                  v-if="selectedOption === index"
                  class="h-3 w-3 rounded-full"
                  :class="getOptionDotClass(index)"
                ></div>
              </div>
              <span class="font-medium mr-2">{{ String.fromCharCode(65 + index) }}.</span>
              <span>{{ option }}</span>
            </div>
          </div>
        </div>

        <transition name="fade">
          <div v-if="showAnswer" class="mt-6 p-4 rounded-lg" :class="isCorrect ? 'bg-green-50' : 'bg-red-50'">
            <div class="flex items-center mb-2">
              <svg
                v-if="isCorrect"
                class="h-6 w-6 text-green-600 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <svg
                v-else
                class="h-6 w-6 text-red-600 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span class="font-semibold" :class="isCorrect ? 'text-green-900' : 'text-red-900'">
                {{ isCorrect ? '回答正确！' : '回答错误' }}
              </span>
            </div>
            <p class="text-sm text-gray-700 mb-1">
              <span class="font-medium">正确答案：</span>
              {{ String.fromCharCode(65 + currentQuestion.correctAnswer) }}
            </p>
            <p class="text-sm text-gray-700">
              <span class="font-medium">解析：</span>
              {{ currentQuestion.explanation }}
            </p>
          </div>
        </transition>

        <div class="flex items-center justify-between mt-6 pt-6 border-t border-gray-200">
          <button
            @click="previousQuestion"
            :disabled="currentIndex === 0"
            class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一题
          </button>
          
          <button
            v-if="!showAnswer"
            @click="submitAnswer"
            :disabled="selectedOption === null"
            class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            提交答案
          </button>
          
          <button
            v-else
            @click="nextQuestion"
            class="btn-primary"
          >
            {{ currentIndex < questions.length - 1 ? '下一题' : '完成练习' }}
          </button>
        </div>
      </div>

      <div class="card">
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold text-primary-600">{{ stats.answered }}</p>
            <p class="text-sm text-gray-600">已答题目</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-green-600">{{ stats.correct }}</p>
            <p class="text-sm text-gray-600">答对</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-red-600">{{ stats.wrong }}</p>
            <p class="text-sm text-gray-600">答错</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getRandomQuestions } from '@/api/questions'

const router = useRouter()

const practicing = ref(false)
const settings = ref({
  count: 20,
  types: ['single', 'judge']
})

const questions = ref([])
const currentIndex = ref(0)
const selectedOption = ref(null)
const showAnswer = ref(false)
const stats = ref({
  answered: 0,
  correct: 0,
  wrong: 0
})

const currentQuestion = computed(() => questions.value[currentIndex.value])
const progress = computed(() => ((currentIndex.value + 1) / questions.value.length) * 100)
const isCorrect = computed(() => selectedOption.value === currentQuestion.value?.correctAnswer)

const startPractice = async () => {
  try {
    const data = await getRandomQuestions(settings.value.count)
    questions.value = data.results || []
  } catch (error) {
    // 使用模拟数据
    questions.value = generateMockQuestions(settings.value.count)
  }
  
  practicing.value = true
}

const generateMockQuestions = (count) => {
  const mockQuestions = []
  for (let i = 0; i < count; i++) {
    mockQuestions.push({
      id: i + 1,
      type: settings.value.types.includes('single') && Math.random() > 0.5 ? '单选题' : '判断题',
      question: `这是第 ${i + 1} 道随机题目的内容`,
      options: ['选项A', '选项B', '选项C', '选项D'],
      correctAnswer: Math.floor(Math.random() * 4),
      explanation: '这是题目的解析内容'
    })
  }
  return mockQuestions
}

const selectOption = (index) => {
  if (!showAnswer.value) {
    selectedOption.value = index
  }
}

const submitAnswer = () => {
  if (selectedOption.value === null) return
  
  showAnswer.value = true
  stats.value.answered++
  
  if (isCorrect.value) {
    stats.value.correct++
  } else {
    stats.value.wrong++
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    selectedOption.value = null
    showAnswer.value = false
  } else {
    router.push('/user/dashboard')
  }
}

const previousQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    selectedOption.value = null
    showAnswer.value = false
  }
}

const getOptionClass = (index) => {
  if (!showAnswer.value) {
    return selectedOption.value === index
      ? 'border-primary-500 bg-primary-50'
      : 'border-gray-200 hover:border-gray-300'
  }
  
  if (index === currentQuestion.value.correctAnswer) {
    return 'border-green-500 bg-green-50'
  }
  
  if (selectedOption.value === index && !isCorrect.value) {
    return 'border-red-500 bg-red-50'
  }
  
  return 'border-gray-200'
}

const getOptionCircleClass = (index) => {
  if (!showAnswer.value) {
    return selectedOption.value === index ? 'border-primary-500' : 'border-gray-300'
  }
  
  if (index === currentQuestion.value.correctAnswer) {
    return 'border-green-500'
  }
  
  if (selectedOption.value === index && !isCorrect.value) {
    return 'border-red-500'
  }
  
  return 'border-gray-300'
}

const getOptionDotClass = (index) => {
  if (!showAnswer.value) {
    return 'bg-primary-500'
  }
  
  if (index === currentQuestion.value.correctAnswer) {
    return 'bg-green-500'
  }
  
  if (selectedOption.value === index && !isCorrect.value) {
    return 'bg-red-500'
  }
  
  return ''
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
