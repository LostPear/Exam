<template>
  <div class="space-y-6">
    <!-- 页头 -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">用户管理</h1>
      <p class="text-gray-600 mt-1">管理系统用户，查看用户信息和学习数据</p>
    </div>

    <!-- 搜索和筛选 -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <input
            v-model="filters.search"
            type="text"
            class="input-field"
            placeholder="搜索用户名或邮箱..."
          />
        </div>
        <div>
          <select v-model="filters.role" class="input-field">
            <option value="">全部角色</option>
            <option value="user">普通用户</option>
            <option value="admin">管理员</option>
          </select>
        </div>
        <div>
          <select v-model="filters.status" class="input-field">
            <option value="">全部状态</option>
            <option value="active">活跃</option>
            <option value="inactive">不活跃</option>
          </select>
        </div>
        <div>
          <button @click="searchUsers" class="w-full btn-primary">
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                用户信息
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                角色
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                注册时间
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                学习统计
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                状态
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium">
                    {{ user.username.charAt(0).toUpperCase() }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ user.username }}</div>
                    <div class="text-sm text-gray-500">{{ user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="user.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'"
                >
                  {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.createdAt }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">
                  练习: {{ user.stats.practice }} 题
                </div>
                <div class="text-sm text-gray-500">
                  考试: {{ user.stats.exam }} 次
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="user.isActive ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
                >
                  {{ user.isActive ? '活跃' : '不活跃' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button @click="viewUser(user)" class="text-primary-600 hover:text-primary-900">
                  查看
                </button>
                <button @click="editUser(user)" class="text-blue-600 hover:text-blue-900">
                  编辑
                </button>
                <button
                  v-if="user.role !== 'admin'"
                  @click="deleteUser(user.id)"
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          显示 {{ (currentPage - 1) * pageSize + 1 }} 到 {{ Math.min(currentPage * pageSize, totalCount) }} 条，共 {{ totalCount }} 条
        </div>
        <div class="flex space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            上一页
          </button>
          <button
            @click="currentPage++"
            :disabled="currentPage * pageSize >= totalCount"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 查看用户详情模态框 -->
    <div v-if="viewingUser" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">用户详情</h2>
            <button @click="viewingUser = null" class="text-gray-400 hover:text-gray-600">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-6">
            <!-- 基本信息 -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">基本信息</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-500">用户名</p>
                  <p class="text-base text-gray-900">{{ viewingUser.username }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">邮箱</p>
                  <p class="text-base text-gray-900">{{ viewingUser.email }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">角色</p>
                  <p class="text-base text-gray-900">
                    {{ viewingUser.role === 'admin' ? '管理员' : '普通用户' }}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">注册时间</p>
                  <p class="text-base text-gray-900">{{ viewingUser.createdAt }}</p>
                </div>
              </div>
            </div>

            <!-- 学习统计 -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">学习统计</h3>
              <div class="grid grid-cols-3 gap-4">
                <div class="text-center p-4 bg-blue-50 rounded-lg">
                  <p class="text-2xl font-bold text-blue-600">{{ viewingUser.stats.practice }}</p>
                  <p class="text-sm text-gray-600 mt-1">练习题目</p>
                </div>
                <div class="text-center p-4 bg-green-50 rounded-lg">
                  <p class="text-2xl font-bold text-green-600">{{ viewingUser.stats.exam }}</p>
                  <p class="text-sm text-gray-600 mt-1">模拟考试</p>
                </div>
                <div class="text-center p-4 bg-purple-50 rounded-lg">
                  <p class="text-2xl font-bold text-purple-600">{{ viewingUser.stats.accuracy }}%</p>
                  <p class="text-sm text-gray-600 mt-1">正确率</p>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-6 flex justify-end">
            <button @click="viewingUser = null" class="btn-primary">
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑用户模态框 -->
    <div v-if="editingUser" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-md w-full">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">编辑用户</h2>
            <button @click="editingUser = null" class="text-gray-400 hover:text-gray-600">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveUser" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
              <input v-model="userForm.username" type="text" class="input-field" required />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input v-model="userForm.email" type="email" class="input-field" required />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">角色</label>
              <select v-model="userForm.role" class="input-field" required>
                <option value="user">普通用户</option>
                <option value="admin">管理员</option>
              </select>
            </div>

            <div>
              <label class="flex items-center">
                <input
                  v-model="userForm.isActive"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <span class="ml-2 text-sm text-gray-700">激活状态</span>
              </label>
            </div>

            <div class="flex items-center justify-end space-x-4 pt-4">
              <button type="button" @click="editingUser = null" class="btn-secondary">
                取消
              </button>
              <button type="submit" class="btn-primary">
                保存修改
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { getUsers, updateUser as apiUpdateUser, deleteUser as apiDeleteUser } from '@/api/users'

const users = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const filters = reactive({
  search: '',
  role: '',
  status: ''
})

const viewingUser = ref(null)
const editingUser = ref(null)

const userForm = reactive({
  username: '',
  email: '',
  role: 'user',
  isActive: true
})

onMounted(() => {
  loadUsers()
})

watch(currentPage, () => {
  loadUsers()
})

const loadUsers = async () => {
  try {
    const data = await getUsers({
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    })
    users.value = data.results || []
    totalCount.value = data.count || 0
  } catch (error) {
    // 使用模拟数据
    users.value = Array.from({ length: 10 }, (_, i) => ({
      id: i + 1,
      username: `user${i + 1}`,
      email: `user${i + 1}@example.com`,
      role: i === 0 ? 'admin' : 'user',
      isActive: i % 3 !== 0,
      createdAt: '2024-03-15',
      stats: {
        practice: Math.floor(Math.random() * 200),
        exam: Math.floor(Math.random() * 20),
        accuracy: Math.floor(Math.random() * 30) + 70
      }
    }))
    totalCount.value = 100
  }
}

const searchUsers = () => {
  currentPage.value = 1
  loadUsers()
}

const viewUser = (user) => {
  viewingUser.value = user
}

const editUser = (user) => {
  editingUser.value = user
  userForm.username = user.username
  userForm.email = user.email
  userForm.role = user.role
  userForm.isActive = user.isActive
}

const saveUser = async () => {
  try {
    await apiUpdateUser(editingUser.value.id, userForm)
    editingUser.value = null
    loadUsers()
  } catch (error) {
    alert('保存失败，请重试')
  }
}

const deleteUser = async (id) => {
  if (!confirm('确定要删除该用户吗？此操作不可撤销。')) return

  try {
    await apiDeleteUser(id)
    loadUsers()
  } catch (error) {
    alert('删除失败，请重试')
  }
}
</script>
