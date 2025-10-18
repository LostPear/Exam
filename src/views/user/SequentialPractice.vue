<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- 顶部进度条 -->
    <div class="card">
      <div class="flex items-center justify-between mb-2">
        <h2 class="text-lg font-semibold text-gray-900">顺序练习</h2>
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
      <!-- 题目类型标签 -->
      <div class="flex items-center justify-between mb-4">
        <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
          {{ currentQuestion.type }}
        </span>
        <button
          @click="toggleBookmark"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg
            class="h-6 w-6"
            :class="currentQuestion.bookmarked ? 'text-yellow-500 fill-current' : 'text-gray-400'"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
        </button>
      </div>

      <!-- 题目内容 -->
      <div class="mb-6">
        <h3 class="text-xl font-medium text-gray-900 mb-4">
          {{ currentQuestion.question }}
        </h3>
        <img
          v-if="currentQuestion.image"
          :src="currentQuestion.image"
          alt="题目图片"
          class="max-w-full h-auto rounded-lg mb-4"
        />
      </div>

      <!-- 选项 -->
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

      <!-- 答案解析 -->
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

      <!-- 操作按钮 -->
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

    <!-- 练习统计 -->
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSequentialQuestions } from '@/api/questions'

const router = useRouter()

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

onMounted(async () => {
  await loadQuestions()
})

const loadQuestions = async () => {
  try {
    const data = await getSequentialQuestions({ limit: 50 })
    questions.value = data.results || []
  } catch (error) {
    // 使用模拟数据
    questions.value = [
      {
        id: 1,
        type: '单选题',
        question: '机动车在道路上发生故障，难以移动时，首先应当持续开启危险报警闪光灯，并在车后多少米处设置警告标志？',
        options: ['50米至100米', '150米以外', '100米至150米', '50米以内'],
        correctAnswer: 0,
        explanation: '根据《道路交通安全法实施条例》规定，机动车在道路上发生故障或者发生交通事故，难以移动时，应当持续开启危险报警闪光灯，并在来车方向设置警告标志等措施扩大示警距离，必要时迅速报警。在高速公路上要在车后150米外设置警告标志，在普通公路上要在车后50米至100米处设置警告标志。',
        bookmarked: false
      },
      {
        id: 2,
        type: '判断题',
        question: '驾驶机动车在道路上行驶时，应当悬挂机动车号牌，放置检验合格标志、保险标志，并随车携带机动车行驶证。',
        options: ['正确', '错误'],
        correctAnswer: 0,
        explanation: '这是法律规定的要求，驾驶机动车上路必须具备这些条件。',
        bookmarked: false
      }
    ]
  }
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
    // 完成练习，跳转到结果页
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

const toggleBookmark = () => {
  currentQuestion.value.bookmarked = !currentQuestion.value.bookmarked
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
