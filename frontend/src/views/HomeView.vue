<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 外部コンポーネント
import JapanMap3D from '../components/japanmap_3D.vue'
import SmartCalendar from '../components/calendar.vue'
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'

const router = useRouter() 

const selectedPref = ref(null)
const showModal = ref(false)
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

// TOPに戻る
const goBack = () => {
  router.push('/')
}
</script>

<template>
  <SnowEffect />

  <div class="home-container">
    <OceanBackground />

    <button class="back-btn" @click="goBack">
      ⬅ TOP
    </button>

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
          <p class="guide-text">シミュレーションする日付を選んでください👇</p>
        </div>
        
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
   バックボタン
   ======================================= */
.back-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 100;
  
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.5);
  color: #fff;
  padding: 15px 30px; /* 大きくしました */
  border-radius: 30px;
  font-weight: bold;
  cursor: pointer;
  backdrop-filter: blur(5px);
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  font-size: 1.2rem; /* 大きくしました */
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: translateX(-3px);
}

/* =======================================
   ホーム画面全体のスタイル
   ======================================= */
.home-container {
  text-align: center;
  padding-bottom: 50px;
  min-height: 100vh;
  position: relative; 
  z-index: 10;
  color: #e3f2fd;
  overflow: hidden; 
}

main {
  position: relative;
  z-index: 5; 
}

header {
  margin-bottom: 20px;
  margin-top: 20px;
  position: relative;
  z-index: 20;
}

h1 {
  color: #bbdefb;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* =======================================
   モーダルのスタイル (BattleViewに合わせました)
   ======================================= */
.modal-overlay {
  position: fixed; 
  top: 0; left: 0; 
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex; justify-content: center; align-items: center;
  z-index: 3000;
  animation: fadeIn 0.3s;
}

.modal-content {
  /* 背景を白に変更 */
  background: #fff; 
  color: #333;
  padding: 25px;
  border-radius: 20px;
  width: 95%; max-width: 500px;
  position: relative;
  animation: popUp 0.4s;
  /* 影などの調整 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute; top: 15px; right: 20px;
  background: none; border: none;
  font-size: 2rem;
  color: #555; /* 色を少し濃く */
  cursor: pointer;
}

.modal-header { 
  margin-bottom: 20px; 
}
.modal-header h2 { 
  margin: 0; 
  color: #1565c0; 
}
.guide-text { 
  margin-top: 5px; 
  font-weight: bold;
  color: #666;
}

.calendar-wrapper { 
  margin-bottom: 10px; 
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes popUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>