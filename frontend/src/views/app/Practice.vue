<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function startSequential() {
  router.push({ name: 'practice-session', query: { mode: 'sequential' } })
}
function startRandom() {
  router.push({ name: 'practice-session', query: { mode: 'random' } })
}
</script>

<template>
  <div class="grid gap-4 sm:grid-cols-2">
    <button class="bg-blue-600 text-white rounded p-6 hover:bg-blue-700" @click="startSequential">
      顺序练习
    </button>
    <button class="bg-green-600 text-white rounded p-6 hover:bg-green-700" @click="startRandom">
      随机练习
    </button>
  </div>
</template>
