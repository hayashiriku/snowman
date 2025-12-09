<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()   // URLのパラメータを受け取る用
const router = useRouter() // ページ移動用

// データ定義
const result = ref(null)
const isLoading = ref(true)
const errorMsg = ref('')

// 比較対象リスト
const comparisons = [
  { name: '人間', height: 1.7, icon: '🧍' },
  { name: 'キリン', height: 5.0, icon: '🦒' },
  { name: '鎌倉の大仏', height: 13.35, icon: '🧘' },
  { name: '通天閣', height: 108, icon: '🗼' },
  { name: '東京タワー', height: 333, icon: '🗼' },
  { name: 'スカイツリー', height: 634, icon: '🏙️' },
  { name: '富士山', height: 3776, icon: '🗻' },
  { name: 'エベレスト', height: 8848, icon: '🏔️' },
]

// 画面が表示されたら自動で計算開始
onMounted(async () => {
  // URLから条件を取得 (?pref=20&date=2024-01-01&type=day)
  const { pref, date, type } = route.query

  if (!pref || !date || !type) {
    errorMsg.value = "条件が不足しています"
    isLoading.value = false
    return
  }

  try {
    const response = await fetch('http://localhost:8000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prefecture_id: parseInt(pref),
        target_date: date,
        period_type: type
      })
    })
    const data = await response.json()
    if (data.error) errorMsg.value = data.error
    else result.value = data
  } catch (e) {
    errorMsg.value = "サーバーエラー"
  } finally {
    isLoading.value = false
  }
})

// --- ビジュアル計算ロジック (App.vueから移動) ---
const bestComparison = computed(() => {
  if (!result.value) return comparisons[0]
  const h = result.value.height_m
  const target = comparisons.find(c => c.height >= h * 0.3) 
  return target || comparisons[comparisons.length - 1]
})

const displayScale = computed(() => {
  if (!result.value) return 1
  const maxHeight = Math.max(result.value.height_m, bestComparison.value.height)
  return maxHeight > 0 ? (300 / maxHeight) : 1
})

const goBack = () => {
  router.push('/') // トップページに戻る
}
</script>

<template>
  <div class="result-page">
    <div v-if="isLoading" class="loading">
      <h2>⛄ 雪を集めています...</h2>
      <div class="spinner">❄️</div>
    </div>

    <div v-else-if="errorMsg" class="error">
      <p>{{ errorMsg }}</p>
      <button @click="goBack">戻る</button>
    </div>

    <div v-else-if="result" class="content">
      <div class="header-area">
        <h1>🎉 完成！</h1>
        <p class="pref-name">{{ result.message }}</p>
      </div>

      <div class="visual-stage">
        <div class="figure-wrapper">
          <div class="comparison-icon" :style="{ fontSize: Math.max(20, bestComparison.height * displayScale) + 'px' }">
            {{ bestComparison.icon }}
          </div>
          <div class="label">{{ bestComparison.name }}<br>({{ bestComparison.height }}m)</div>
        </div>

        <div class="figure-wrapper">
          <div class="snowman-figure" :style="{ height: (result.height_m * displayScale) + 'px' }">
            <div class="head"></div><div class="body"></div>
          </div>
          <div class="label highlight">{{ result.height_m.toFixed(1) }}m</div>
        </div>
      </div>

      <div class="stats-box">
        <p>体積: <strong>{{ result.volume_m3.toLocaleString() }}</strong> m³</p>
      </div>

      <button class="back-btn" @click="goBack">もう一度作る</button>
    </div>
  </div>
</template>

<style scoped>
/* App.vue からスタイルを移植して調整 */
.result-page { text-align: center; padding: 20px; font-family: sans-serif; min-height: 100vh; background: linear-gradient(to bottom, #e3f2fd, #fff); }
.visual-stage { display: flex; align-items: flex-end; justify-content: center; gap: 40px; border-bottom: 10px solid #795548; height: 400px; margin: 30px auto; max-width: 800px; }
.figure-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; width: 120px; }
.snowman-figure { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; }
.head, .body { width: 100%; background: radial-gradient(circle at 30% 30%, #fff, #eceff1); border: 1px solid #b0bec5; border-radius: 50%; box-shadow: 2px 5px 10px rgba(0,0,0,0.1); }
.head { height: 44%; aspect-ratio: 1/1; z-index: 2; margin-bottom: -15%; }
.body { height: 56%; aspect-ratio: 1/1; z-index: 1; }
.comparison-icon { line-height: 1; transform-origin: bottom; }
.back-btn { background: #0288d1; color: white; border: none; padding: 15px 40px; border-radius: 50px; font-size: 1.2rem; font-weight: bold; cursor: pointer; margin-top: 20px; transition: transform 0.2s; box-shadow: 0 5px 15px rgba(2,136,209,0.3); }
.back-btn:hover { transform: scale(1.05); }
.loading { margin-top: 100px; color: #0288d1; }
.spinner { font-size: 3rem; animation: spin 2s infinite linear; display: inline-block; margin-top: 20px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>