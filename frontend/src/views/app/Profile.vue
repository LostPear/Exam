<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const email = ref('')
const username = ref('')
const password = ref('')

onMounted(async () => {
  await auth.fetchMe()
  email.value = auth.currentUser?.email || ''
  username.value = auth.currentUser?.username || ''
})

async function onSubmit() {
  await auth.updateProfile({ email: email.value, username: username.value, password: password.value || undefined })
}
</script>

<template>
  <form class="space-y-4 max-w-lg" @submit.prevent="onSubmit">
    <div>
      <label class="block text-sm font-medium mb-1">邮箱</label>
      <input v-model="email" type="email" class="w-full rounded border p-2" />
    </div>
    <div>
      <label class="block text-sm font-medium mb-1">用户名</label>
      <input v-model="username" type="text" class="w-full rounded border p-2" />
    </div>
    <div>
      <label class="block text-sm font-medium mb-1">新密码（可选）</label>
      <input v-model="password" type="password" class="w-full rounded border p-2" />
    </div>
    <button class="bg-blue-600 text-white rounded px-4 py-2">保存</button>
  </form>
</template>
