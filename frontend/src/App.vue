<script setup>
import { ref, onMounted } from 'vue'

const message = ref('読み込み中...')

onMounted(async () => {
  try {
    // Pythonサーバー(8000番)にデータを取りに行く
    const res = await fetch('http://localhost:8000/')
    const data = await res.json()
    message.value = data.message
  } catch (error) {
    message.value = 'エラー！サーバーが動いていません'
  }
})
</script>

<template>
  <div style="text-align: center; margin-top: 50px;">
    <h1>{{ message }}</h1>
  </div>
</template>