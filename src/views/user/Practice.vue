<template>
  <div class="space-y-6">
    <div class="card">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">练习模式</h1>
      <p class="text-gray-600">选择练习方式，提升您的驾照理论知识</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 顺序练习 -->
      <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push('/user/practice/sequential')">
        <div class="flex items-center justify-center h-32 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg mb-4">
          <svg class="h-16 w-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">顺序练习</h2>
        <p class="text-gray-600 mb-4">按照题库顺序依次练习，系统记录您的练习进度</p>
        <div class="flex items-center text-primary-600 font-medium">
          开始练习
          <svg class="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>

      <!-- 随机练习 -->
      <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push('/user/practice/random')">
        <div class="flex items-center justify-center h-32 bg-gradient-to-br from-green-500 to-green-600 rounded-lg mb-4">
          <svg class="h-16 w-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">随机练习</h2>
        <p class="text-gray-600 mb-4">随机抽取题目进行练习，加强知识点巩固</p>
        <div class="flex items-center text-primary-600 font-medium">
          开始练习
          <svg class="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 练习统计 -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 mb-4">练习统计</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="text-center p-4 bg-blue-50 rounded-lg">
          <p class="text-2xl font-bold text-blue-600">{{ practiceStats.total }}</p>
          <p class="text-sm text-gray-600 mt-1">已练习题目</p>
        </div>
        <div class="text-center p-4 bg-green-50 rounded-lg">
          <p class="text-2xl font-bold text-green-600">{{ practiceStats.correct }}</p>
          <p class="text-sm text-gray-600 mt-1">答对题目</p>
        </div>
        <div class="text-center p-4 bg-red-50 rounded-lg">
          <p class="text-2xl font-bold text-red-600">{{ practiceStats.wrong }}</p>
          <p class="text-sm text-gray-600 mt-1">答错题目</p>
        </div>
        <div class="text-center p-4 bg-purple-50 rounded-lg">
          <p class="text-2xl font-bold text-purple-600">{{ practiceStats.accuracy }}%</p>
          <p class="text-sm text-gray-600 mt-1">正确率</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const practiceStats = ref({
  total: 156,
  correct: 132,
  wrong: 24,
  accuracy: 85
})

onMounted(() => {
  // 加载练习统计数据
})
</script>
