<script setup>
import { ref, computed } from 'vue'
import JapanMap3D from './components/japanmap_3D.vue'

// --- データ ---
const selectedPref = ref(null)
const showModal = ref(false)
const targetDate = ref('2024-01-01')
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
        target_date: targetDate.value,
        period_type: periodType.value
      })
    })

    const data = await response.json()
    if (data.error) {
      errorMsg.value = data.error
    } else {
      result.value = data
    }
  } catch (e) {
    errorMsg.value = "サーバーエラーが発生しました"
  } finally {
    isLoading.value = false
  }
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
      <h1>⛄ 雪だるまメーカー</h1>
      <p>地図のピンをクリックして場所を選んでね</p>
    </header>

    <main>
      <JapanMap3D @select="handleMapSelect" />
    </main>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        
        <h2>📍 {{ selectedPref.name }}</h2>
        <p class="subtitle">いつの雪で作りますか？</p>

        <div class="control-panel">
          <div class="input-group">
            <label>日付</label>
            <input type="date" v-model="targetDate">
          </div>
          <div class="input-group">
            <label>期間</label>
            <select v-model="periodType">
              <option value="day">1日 (積雪深)</option>
              <option value="month">1ヶ月 (降雪量)</option>
              <option value="year">1年 (年間合計)</option>
            </select>
          </div>
          <button class="calc-btn" @click="calculate" :disabled="isLoading">
            {{ isLoading ? '計算中...' : '雪を集める！' }}
          </button>
        </div>

        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

        <div v-if="result" class="result-box">
          <div class="message">{{ result.message }}</div>
          
          <div class="stats">
            <div>高さ: <strong>{{ result.height_m.toFixed(2) }}m</strong></div>
            <div>体積: {{ result.volume_m3.toFixed(0) }}m³</div>
          </div>

          <div class="visual-stage">
            <div class="figure-wrapper">
              <div class="human-icon">🧍</div>
              <div class="label">1.7m</div>
            </div>
            <div class="figure-wrapper">
              <div class="snowman-figure" :style="{ height: snowmanHeightPx + 'px' }">
                <div class="head"></div>
                <div class="body"></div>
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
.app-container { text-align: center; font-family: sans-serif; color: #333; padding-bottom: 50px; }
header { margin-bottom: 30px; }
h1 { color: #0288d1; margin: 0; }

/* モーダル */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center; z-index: 999;
  animation: fadeIn 0.3s;
}
.modal-content {
  background: white; padding: 30px; border-radius: 16px; width: 90%; max-width: 550px;
  position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  max-height: 90vh; overflow-y: auto;
  animation: popUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.close-btn { position: absolute; top: 15px; right: 20px; border: none; background: none; font-size: 2rem; cursor: pointer; color: #999; }
.subtitle { color: #666; margin-bottom: 20px; }

.control-panel { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; align-items: flex-end; flex-wrap: wrap;}
.input-group { display: flex; flex-direction: column; text-align: left; }
input, select { padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
.calc-btn { background: #0288d1; color: white; border: none; padding: 12px 24px; border-radius: 30px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.calc-btn:hover { background: #0277bd; transform: scale(1.05); }
.calc-btn:disabled { background: #ccc; cursor: not-allowed; }

.result-box { margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; }
.message { background: #e1f5fe; color: #0277bd; padding: 10px; border-radius: 8px; margin-bottom: 15px; display: inline-block; font-weight: bold;}
.stats { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; font-size: 1.1rem; }
.error-msg { color: red; margin: 10px 0; }

/* ビジュアル */
.visual-stage { display: flex; align-items: flex-end; justify-content: center; gap: 40px; border-bottom: 5px solid #795548; padding-bottom: 5px; min-height: 250px; }
.figure-wrapper { display: flex; flex-direction: column; align-items: center; }
.human-icon { font-size: 68px; line-height: 1; }
.snowman-figure { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; min-height: 10px; transition: height 0.8s; }
.head, .body { width: 100%; background: radial-gradient(circle at 30% 30%, #fff, #eceff1); border: 1px solid #b0bec5; border-radius: 50%; }
.head { height: 44%; aspect-ratio: 1/1; z-index: 2; margin-bottom: -15%; }
.body { height: 56%; aspect-ratio: 1/1; z-index: 1; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes popUp { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>