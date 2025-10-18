<script setup lang="ts">
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

async function onLogout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen">
    <header class="bg-white shadow">
      <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-semibold">驾照理论考试</h1>
        <nav class="flex items-center gap-4">
          <RouterLink class="text-gray-700 hover:text-blue-600" to="/app/practice">练习</RouterLink>
          <RouterLink class="text-gray-700 hover:text-blue-600" to="/app/exam">模拟考试</RouterLink>
          <RouterLink class="text-gray-700 hover:text-blue-600" to="/app/profile">个人资料</RouterLink>
          <button class="text-red-600" @click="onLogout">退出登录</button>
        </nav>
      </div>
    </header>
    <main class="max-w-6xl mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>
