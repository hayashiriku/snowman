<script setup>
import { ref, computed } from 'vue'
import JapanMap3D from './components/japanmap_3D.vue'
import SmartCalendar from './components/calendar.vue'

// --- データ ---
const selectedPref = ref(null)
const showModal = ref(false)
const targetDate = ref(new Date('2024-01-01'))
const periodType = ref('day')
const result = ref(null)
const isLoading = ref(false)
const errorMsg = ref('')

// --- イベントハンドラ ---

// 地図クリック
const handleMapSelect = (pin) => {
  selectedPref.value = pin
  result.value = null
  errorMsg.value = ''
  showModal.value = true // モーダルを開く
}

// モーダル閉じる
const closeModal = () => {
  showModal.value = false
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// 計算実行
const calculate = async () => {
  isLoading.value = true
  result.value = null
  errorMsg.value = ''

  try {
    const response = await fetch('http://localhost:8000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prefecture_id: selectedPref.value.id,
        target_date: formatDate(targetDate.value),
        period_type: periodType.value
      })
    })

    const data = await response.json()
    if (data.error) errorMsg.value = data.error
    else result.value = data
  } catch (e) {
    errorMsg.value = "サーバー通信エラー"
  } finally {
    isLoading.value = false
  }
}

// ★カレンダーから「どの場所がクリックされたか(type)」を受け取る
const handleSearch = (type) => {
  // モードを切り替える
  periodType.value = type
  
  // UI更新のチラつき防止で少し待つ
  setTimeout(() => calculate(), 50)
}

// 雪だるま高さ (1m = 40px)
const snowmanHeightPx = computed(() => {
  if (!result.value) return 0
  return result.value.height_m * 40
})
</script>

<template>
  <div class="app-container">
    <header>
      <h1>⛄ 雪だるまシミュレーター</h1>
      <p>地図のピンをクリックしてね！</p>
    </header>

    <main>
      <JapanMap3D @select="handleMapSelect" />
    </main>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        
        <div class="modal-header">
          <h2>📍 {{ selectedPref.name }}</h2>
        </div>

        <p class="guide-text">
          年・月・日付、クリックした場所で雪を集めるよ！👇
        </p>

        <div class="calendar-wrapper">
          <SmartCalendar 
            v-model="targetDate"
            @search="handleSearch"
          />
        </div>

        <div v-if="isLoading" class="loading-msg">⛄ 雪を集めています...</div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

        <div v-if="result" class="result-box">
          <div class="message">{{ result.message }}</div>
          <div class="stats">
            <div>高さ: <strong>{{ result.height_m.toFixed(2) }}m</strong></div>
            <div>体積: {{ result.volume_m3.toFixed(0) }}m³</div>
          </div>
          <div class="visual-stage">
            <div class="figure-wrapper">
              <div class="human-icon">🧍</div><div class="label">1.7m</div>
            </div>
            <div class="figure-wrapper">
              <div class="snowman-figure" :style="{ height: snowmanHeightPx + 'px' }">
                <div class="head"></div><div class="body"></div>
              </div>
              <div class="label highlight">{{ result.height_m.toFixed(1) }}m</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* スタイルは前回のままでOKですが、カレンダー用変数は不要になったので削除してOK */
.app-container { text-align: center; font-family: sans-serif; color: #333; padding-bottom: 50px; }
h1 { color: #0288d1; margin: 0; }
header { margin-bottom: 20px; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.6); display: flex; justify-content: center; align-items: center; z-index: 999; backdrop-filter: blur(2px); animation: fadeIn 0.3s; }
.modal-content { background: white; padding: 25px; border-radius: 20px; width: 95%; max-width: 500px; position: relative; box-shadow: 0 25px 50px rgba(0,0,0,0.4); max-height: 90vh; overflow-y: auto; animation: popUp 0.4s; }
.close-btn { position: absolute; top: 15px; right: 20px; background: none; border: none; font-size: 2rem; color: #aaa; cursor: pointer; }
.modal-header { text-align: center; margin-bottom: 15px; }
.guide-text { font-size: 0.9rem; color: #666; margin-bottom: 15px; }
.calendar-wrapper { display: flex; justify-content: center; margin-bottom: 20px; }
.loading-msg { color: #0288d1; font-weight: bold; margin: 10px 0; }
.result-box { border-top: 2px dashed #eee; padding-top: 20px; }
.message { background: #e1f5fe; color: #0277bd; padding: 10px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; display: inline-block;}
.stats { display: flex; justify-content: center; gap: 30px; margin-bottom: 20px; }
.visual-stage { display: flex; align-items: flex-end; justify-content: center; gap: 30px; border-bottom: 6px solid #795548; padding-bottom: 5px; min-height: 250px; }
.figure-wrapper { display: flex; flex-direction: column; align-items: center; }
.human-icon { font-size: 68px; line-height: 1; }
.snowman-figure { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; min-height: 10px; transition: height 0.8s; }
.head, .body { width: 100%; background: radial-gradient(circle at 30% 30%, #fff, #eceff1); border: 1px solid #b0bec5; border-radius: 50%; box-shadow: 2px 5px 10px rgba(0,0,0,0.1); }
.head { height: 44%; aspect-ratio: 1/1; z-index: 2; margin-bottom: -15%; }
.body { height: 56%; aspect-ratio: 1/1; z-index: 1; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes popUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>