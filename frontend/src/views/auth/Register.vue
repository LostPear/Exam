<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const email = ref('')
const username = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  try {
    await auth.register({ email: email.value, username: username.value, password: password.value })
    // redirect to login after successful register
    router.push({ name: 'login' })
  } catch (e) {
    // error is shown below
  }
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="onSubmit">
    <div>
      <label class="block text-sm font-medium mb-1">邮箱</label>
      <input v-model="email" type="email" class="w-full rounded border p-2 focus:outline-none focus:ring focus:border-blue-400" placeholder="请输入邮箱" />
    </div>
    <div>
      <label class="block text-sm font-medium mb-1">用户名</label>
      <input v-model="username" type="text" class="w-full rounded border p-2 focus:outline-none focus:ring focus:border-blue-400" placeholder="请输入用户名" />
    </div>
    <div>
      <label class="block text-sm font-medium mb-1">密码</label>
      <input v-model="password" type="password" class="w-full rounded border p-2 focus:outline-none focus:ring focus:border-blue-400" placeholder="请输入密码" />
    </div>
    <p v-if="auth.error" class="text-sm text-red-600">{{ auth.error }}</p>
    <button :disabled="auth.loading" type="submit" class="w-full bg-blue-600 text-white rounded py-2 hover:bg-blue-700 disabled:opacity-50">注册</button>
    <div class="text-sm text-center">
      已有账号？
      <RouterLink to="/auth/login" class="text-blue-600 hover:underline">去登录</RouterLink>
    </div>
  </form>
</template>
