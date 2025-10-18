<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { listUsersApi, toggleAdminApi } from '../../services/admin'
import type { User } from '../../types/auth'

const users = ref<User[]>([])

async function load() {
  users.value = await listUsersApi()
}

async function toggle(user: User) {
  await toggleAdminApi(user.id, !user.is_admin)
  await load()
}

onMounted(load)
</script>

<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="font-semibold mb-2">用户列表</h2>
    <table class="w-full text-left">
      <thead>
        <tr class="border-b">
          <th class="p-2">ID</th>
          <th class="p-2">用户名</th>
          <th class="p-2">邮箱</th>
          <th class="p-2">管理员</th>
          <th class="p-2">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id" class="border-b">
          <td class="p-2">{{ u.id }}</td>
          <td class="p-2">{{ u.username }}</td>
          <td class="p-2">{{ u.email }}</td>
          <td class="p-2">{{ u.is_admin ? '是' : '否' }}</td>
          <td class="p-2">
            <button class="text-blue-600" @click="toggle(u)">{{ u.is_admin ? '取消管理员' : '设为管理员' }}</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
