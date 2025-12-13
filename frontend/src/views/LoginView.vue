<script setup>
import { useRouter } from 'vue-router'

// 共通の背景・エフェクトコンポーネント
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'

const router = useRouter()

// モード選択処理
const handleStart = (mode) => {
  if (mode === 'simulation') {
    // 地図画面へ
    router.push('/home') 
  } else if (mode === 'battle') {
    // バトル画面へ（仮）
    router.push('/battle') 
  }
}
</script>

<template>
  <SnowEffect />
  <div class="start-container">
    <OceanBackground />

    <div class="start-card">
      <div class="icon-area">
        <span class="snowman-icon">⛄</span>
      </div>
      <h1>Snowman Simulator</h1>
      <p class="subtitle">遊ぶモードを選んでスタート！</p>

      <div class="mode-select-area">
        <button 
          type="button" 
          class="mode-btn simulation-btn" 
          @click="handleStart('simulation')"
        >
          <span class="btn-icon">❄️</span>
          <div class="btn-text">
            <span class="main-label">Simulation</span>
            <span class="sub-label">雪だるまを作る</span>
          </div>
        </button>

        <button 
          type="button" 
          class="mode-btn battle-btn" 
          @click="handleStart('battle')"
        >
          <span class="btn-icon">⚔️</span>
          <div class="btn-text">
            <span class="main-label">Battle Mode</span>
            <span class="sub-label">雪合戦で戦う</span>
          </div>
        </button>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* 全体のレイアウト */
.start-container {
  min-height: 100vh;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 10;
}

/* グラスモーフィズムカード */
.start-card {
  position: relative;
  z-index: 20;
  background: rgba(255, 255, 255, 0.15); /* 半透明の白 */
  backdrop-filter: blur(10px); /* すりガラス効果 */
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 50px 40px;
  border-radius: 30px;
  width: 90%;
  max-width: 420px;
  text-align: center;
  box-shadow: 0 8px 32px 0 rgba(0, 37, 93, 0.37);
  color: #fff;
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.icon-area {
  font-size: 4rem;
  margin-bottom: 10px;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
  animation: bounce 2s infinite;
}

h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #fff;
  text-shadow: 0 2px 5px rgba(0,0,0,0.3);
  letter-spacing: 1px;
}

.subtitle {
  margin-top: 10px;
  margin-bottom: 30px;
  color: #e3f2fd;
  font-size: 1rem;
}

/* モード選択エリア */
.mode-select-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 10px;
}

.mode-btn {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border: none;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
  text-align: left;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  position: relative;
  overflow: hidden;
}

.mode-btn:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.mode-btn:active { transform: translateY(0); }

.btn-icon {
  font-size: 2rem;
  margin-right: 18px;
  filter: drop-shadow(0 2px 2px rgba(0,0,0,0.2));
}

.btn-text {
  display: flex;
  flex-direction: column;
}

.main-label {
  font-size: 1.2rem;
  font-weight: bold;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.sub-label {
  font-size: 0.8rem;
  opacity: 0.9;
  margin-top: 2px;
}

/* シミュレーションボタン (青系) */
.simulation-btn {
  background: linear-gradient(135deg, #4fc3f7, #0288d1);
  border: 1px solid rgba(255,255,255,0.2);
}

/* バトルボタン (赤/オレンジ系) */
.battle-btn {
  background: linear-gradient(135deg, #ff8a65, #d84315);
  border: 1px solid rgba(255,255,255,0.2);
}

/* アニメーション定義 */
@keyframes popIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>