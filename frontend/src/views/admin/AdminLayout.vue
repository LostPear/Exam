<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function toUserMode() {
  router.push('/app')
}
</script>

<template>
  <div>
    <header class="bg-gray-900 text-white">
      <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-semibold">后台管理</h1>
        <nav class="flex gap-4 items-center">
          <RouterLink to="/admin/questions" class="hover:underline">题库管理</RouterLink>
          <RouterLink to="/admin/users" class="hover:underline">用户管理</RouterLink>
          <RouterLink to="/admin/import" class="hover:underline">题库导入</RouterLink>
          <button class="bg-gray-700 px-3 py-1 rounded" @click="toUserMode">返回用户端</button>
        </nav>
      </div>
    </header>
    <main class="max-w-6xl mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>
