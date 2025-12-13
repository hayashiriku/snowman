<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 外部コンポーネントのインポート
// ファイルパスは実際のプロジェクト構成に合わせて適宜調整してください
import JapanMap3D from '../components/japanmap_3D.vue'
import SmartCalendar from '../components/calendar.vue'
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'

const router = useRouter() // ページ移動用

const selectedPref = ref(null)
const showModal = ref(false)
// 初期日付（必要に応じて変更してください）
const targetDate = ref(new Date('2024-01-01'))

// 地図クリック
const handleMapSelect = (pin) => {
  selectedPref.value = pin
  showModal.value = true
}

const closeModal = () => showModal.value = false

// 日付フォーマット
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// ページ移動
const handleSearch = (type) => {
  router.push({
    path: '/result',
    query: {
      pref: selectedPref.value.id,
      prefName: selectedPref.value.name,
      date: formatDate(targetDate.value),
      type: type
    }
  })
}
</script>

<template>
  <SnowEffect />

  <div class="home-container">
    <OceanBackground />

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
        <p class="guide-text">クリックすると結果画面へ移動します👇</p>
        
        <div class="calendar-wrapper">
          <SmartCalendar 
            v-model="targetDate" 
            :prefId="selectedPref?.id" 
            @search="handleSearch" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* =======================================
   ホーム画面全体のスタイル
   ======================================= */
.home-container {
  text-align: center;
  padding-bottom: 50px;
  /* 海背景を表示するために高さ確保と相対配置を設定 */
  min-height: 100vh;
  position: relative; 
  z-index: 10;
  /* 文字色を背景に合わせて調整 */
  color: #e3f2fd;
  overflow: hidden; /* 波がはみ出さないように */
}

/* =======================================
   Main (地図エリア)
   OceanBackground(z-index:1) より手前に配置し、
   地図がクリック可能であることを保証する
   ======================================= */
main {
  position: relative;
  z-index: 5; 
}

/* =======================================
   ヘッダー
   ======================================= */
header {
  margin-bottom: 20px;
  margin-top: 20px;
  position: relative;
  z-index: 20;
}

h1 {
  /* 濃い青背景でも見える明るい色に変更 */
  color: #bbdefb;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* =======================================
   モーダル
   ======================================= */
.modal-overlay {
  position: fixed; 
  top: 0; left: 0; 
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex; justify-content: center; align-items: center;
  /* 雪(9000)よりは下だが、他の要素より上 */
  z-index: 3000;
  animation: fadeIn 0.3s;
}

.modal-content {
  /* 海背景に合う少し明るい青系の白、または白 */
  background: #f0f8ff; 
  padding: 25px;
  border-radius: 20px;
  width: 95%; max-width: 500px;
  position: relative;
  animation: popUp 0.4s;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  color: #333; /* モーダル内の文字色は読みやすく黒系に戻す */
}

.close-btn {
  position: absolute; top: 15px; right: 20px;
  background: none; border: none;
  font-size: 2rem;
  color: #1a237e;
  cursor: pointer;
}

.modal-header { 
  text-align: center; 
  margin-bottom: 15px; 
}

.modal-header h2 {
  color: #1a237e;
  margin: 0;
}

.guide-text {
  font-size: 0.9rem;
  color: #1565c0;
  margin-bottom: 15px;
}

.calendar-wrapper { 
  display: flex; 
  justify-content: center; 
  margin-bottom: 20px; 
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes popUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>