<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { listQuestionsApi, createQuestionApi, deleteQuestionApi } from '../../services/questions'
import type { Question } from '../../types/questions'

const questions = ref<Question[]>([])
const newContent = ref('')
const newOptions = ref('') // comma separated
const newAnswer = ref(0)

async function load() {
  questions.value = await listQuestionsApi()
}

async function create() {
  const payload = {
    content: newContent.value,
    options: newOptions.value.split(',').map(s => s.trim()),
    answer: newAnswer.value,
  }
  await createQuestionApi(payload)
  newContent.value = ''
  newOptions.value = ''
  newAnswer.value = 0
  await load()
}

async function remove(id: number) {
  await deleteQuestionApi(id)
  await load()
}

onMounted(load)
</script>

<template>
  <div class="space-y-6">
    <div class="bg-white p-4 rounded shadow space-y-2">
      <h2 class="font-semibold">新增题目</h2>
      <input v-model="newContent" placeholder="题目内容" class="w-full rounded border p-2" />
      <input v-model="newOptions" placeholder="选项（用英文逗号分隔）" class="w-full rounded border p-2" />
      <input v-model.number="newAnswer" type="number" min="0" placeholder="正确答案索引" class="w-40 rounded border p-2" />
      <button class="bg-blue-600 text-white rounded px-4 py-2" @click="create">创建</button>
    </div>

    <div class="bg-white p-4 rounded shadow">
      <h2 class="font-semibold mb-2">题库</h2>
      <table class="w-full text-left">
        <thead>
          <tr class="border-b">
            <th class="p-2">ID</th>
            <th class="p-2">内容</th>
            <th class="p-2">选项</th>
            <th class="p-2">答案</th>
            <th class="p-2">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="q in questions" :key="q.id" class="border-b">
            <td class="p-2">{{ q.id }}</td>
            <td class="p-2">{{ q.content }}</td>
            <td class="p-2">{{ q.options.join(', ') }}</td>
            <td class="p-2">{{ q.answer }}</td>
            <td class="p-2">
              <button class="text-red-600" @click="remove(q.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
