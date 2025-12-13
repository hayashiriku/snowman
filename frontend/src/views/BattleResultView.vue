<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// 共通コンポーネント
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'

// ★画像ファイルのインポート（1枚だけでOK！）
// ファイル名が違う場合（.pngなど）はここを書き換えてください
import snowmanImg from '/public/snowman.svg'

const route = useRoute()
const router = useRouter()

// パラメータ取得
const p1 = {
  name: route.query.p1_name || 'Player 1',
  date: route.query.p1_label || '日付不明',
  id: route.query.p1_id
}
const p2 = {
  name: route.query.p2_name || 'Player 2',
  date: route.query.p2_label || '日付不明',
  id: route.query.p2_id
}

// ==========================================
// バトル状態管理
// ==========================================
const battleState = ref('ready') // ready, fighting, finished
const winner = ref(null)

// 各プレイヤーのHP (100スタート)
const p1Hp = ref(100)
const p2Hp = ref(100)

// アニメーション用クラス管理
const p1Action = ref('idle')
const p2Action = ref('idle')

// 攻撃エフェクト（雪玉）の表示フラグ
const showSnowballP1 = ref(false)
const showSnowballP2 = ref(false)

// ==========================================
// 戦闘ロジック
// ==========================================
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const startBattleSequence = async () => {
  await sleep(1000)
  battleState.value = 'fighting'

  while (p1Hp.value > 0 && p2Hp.value > 0) {
    const isP1Turn = Math.random() > 0.5
    if (isP1Turn) {
      await performAttack(1)
    } else {
      await performAttack(2)
    }
    await sleep(800)
  }
  finishBattle()
}

const performAttack = async (attacker) => {
  // 1. 攻撃モーション
  if (attacker === 1) {
    p1Action.value = 'attack' 
    showSnowballP1.value = true
  } else {
    p2Action.value = 'attack' 
    showSnowballP2.value = true
  }

  // 2. ダメージ発生
  await sleep(300)
  const dmg = Math.floor(Math.random() * 15) + 15

  if (attacker === 1) {
    p2Action.value = 'damage'
    p2Hp.value = Math.max(0, p2Hp.value - dmg)
    showSnowballP1.value = false
  } else {
    p1Action.value = 'damage'
    p1Hp.value = Math.max(0, p1Hp.value - dmg)
    showSnowballP2.value = false
  }

  // 3. 戻る
  await sleep(500)
  p1Action.value = 'idle'
  p2Action.value = 'idle'
}

const finishBattle = () => {
  battleState.value = 'finished'
  winner.value = p1Hp.value > 0 ? 1 : 2
}

onMounted(() => {
  startBattleSequence()
})

const goBackHome = () => router.push('/home')
const goBackBattle = () => router.push('/battle')
const goTop = () => router.push('/')
</script>

<template>
  <SnowEffect />
  
  <div class="battle-result-container">
    <OceanBackground />

    <div class="player-panel p1" :class="{ 'loser': battleState === 'finished' && winner === 2 }">
      <div class="hp-bar-container">
        <div class="hp-bar-fill red" :style="{ width: p1Hp + '%' }"></div>
      </div>
      
      <div class="avatar-wrapper">
        <img 
          :src="snowmanImg" 
          alt="Red Snowman" 
          class="snowman-img red-tint" 
          :class="p1Action"
        />
        <div v-if="showSnowballP1" class="flying-snowball to-right">❄️</div>
      </div>

      <div class="info-box">
        <h2 class="pref-name">{{ p1.name }}</h2>
        <p class="date-text">{{ p1.date }}</p>
      </div>
    </div>

    <div class="center-area">
      <div v-if="battleState === 'ready'" class="vs-logo">VS</div>
      <div v-else-if="battleState === 'fighting'" class="clash-effect">⚔️</div>
      <div v-else-if="battleState === 'finished'" class="result-badge">
        <div class="crown">👑</div>
        <div class="winner-text">WINNER</div>
        <div class="winner-name">
          {{ winner === 1 ? '先攻 (RED)' : '後攻 (BLUE)' }}
        </div>
      </div>
    </div>

    <div class="player-panel p2" :class="{ 'loser': battleState === 'finished' && winner === 1 }">
      <div class="hp-bar-container">
        <div class="hp-bar-fill blue" :style="{ width: p2Hp + '%' }"></div>
      </div>

      <div class="avatar-wrapper">
        <img 
          :src="snowmanImg" 
          alt="Blue Snowman" 
          class="snowman-img blue-tint flipped" 
          :class="p2Action"
        />
        <div v-if="showSnowballP2" class="flying-snowball to-left">❄️</div>
      </div>

      <div class="info-box">
        <h2 class="pref-name">{{ p2.name }}</h2>
        <p class="date-text">{{ p2.date }}</p>
      </div>
    </div>

    <div v-if="battleState === 'finished'" class="action-footer">
      <button @click="goBackBattle" class="retry-btn">⚔️ 再戦する</button>
      <button @click="goBackHome" class="home-btn">🗺️ 地図へ</button>
      <button @click="goTop" class="top-btn">🏠 TOP</button>
    </div>

  </div>
</template>

<style scoped>
/* =======================================
   レイアウト
   ======================================= */
.battle-result-container {
  min-height: 100vh;
  position: relative;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  z-index: 10; overflow: hidden; color: #fff;
}

/* =======================================
   プレイヤーパネル
   ======================================= */
.player-panel {
  position: relative; width: 90%; max-width: 500px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px; padding: 15px; margin: 20px 0;
  display: flex; align-items: center; color: #333;
  transition: all 0.5s;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  z-index: 20;
}
.player-panel.loser { filter: grayscale(100%) brightness(0.6); transform: scale(0.9); }
.p1 { border-bottom: 5px solid #ff5252; }
.p2 { border-bottom: 5px solid #448aff; flex-direction: row-reverse; text-align: right; }

.info-box { flex: 1; padding: 0 15px; }
.pref-name { margin: 0; font-size: 1.6rem; color: #222; }
.date-text { margin: 0; font-weight: bold; color: #555; font-size: 0.9rem; }

/* =======================================
   HPゲージ
   ======================================= */
.hp-bar-container {
  position: absolute; top: -10px; left: 10px; right: 10px; height: 10px;
  background: #444; border-radius: 10px; overflow: hidden;
  border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
.hp-bar-fill { height: 100%; transition: width 0.3s ease-out; }
.red { background: #ff1744; }
.blue { background: #2979ff; }

/* =======================================
   雪だるま画像スタイル (重要！)
   ======================================= */
.avatar-wrapper {
  position: relative; width: 100px; height: 100px;
  display: flex; justify-content: center; align-items: center;
  overflow: visible; 
}

.snowman-img {
  width: 100%; height: 100%; object-fit: contain;
  /* 基本アニメーション */
  animation: idle-bounce 1.5s infinite ease-in-out;
  transform-origin: center bottom;
}

/* ★ 1P (赤) のフィルター: 赤い影をつける */
.red-tint {
  filter: drop-shadow(0 0 8px rgba(255, 0, 0, 0.8));
}

/* ★ 2P (青) のフィルター: 青い影をつける */
.blue-tint {
  filter: drop-shadow(0 0 8px rgba(0, 80, 255, 0.8));
}

/* ★ 2Pは画像を反転させて向かい合わせる */
.flipped {
  transform: scaleX(-1); /* 左右反転 */
}
/* 反転した状態での待機アニメーション上書き */
.flipped.idle {
  animation: idle-bounce-flipped 1.5s infinite ease-in-out;
}

/* --- 攻撃アクション --- */
/* 1P: 右へ突撃 */
.p1 .snowman-img.attack { animation: lunge-right 0.3s forwards; }

/* 2P: 左へ突撃 (反転状態からの動作) */
.p2 .snowman-img.attack { animation: lunge-left-flipped 0.3s forwards; }

/* --- ダメージアクション --- */
.damage {
  /* ダメージ時は真っ赤に点滅 */
  animation: shake-damage 0.4s forwards !important;
  filter: sepia(100%) saturate(1000%) hue-rotate(-50deg) !important;
}

/* --- 雪玉 --- */
.flying-snowball { position: absolute; font-size: 2rem; top: 30%; z-index: 30; }
.to-right { left: 60%; animation: fly-right 0.3s linear forwards; }
.to-left { right: 60%; animation: fly-left 0.3s linear forwards; }

/* =======================================
   Keyframes (反転対応版)
   ======================================= */
@keyframes idle-bounce {
  0%, 100% { transform: translateY(0) scale(1, 1); }
  50% { transform: translateY(-5px) scale(1.05, 0.95); }
}
/* 反転時の待機モーション (scaleX(-1)を維持) */
@keyframes idle-bounce-flipped {
  0%, 100% { transform: scaleX(-1) translateY(0) scale(1, 1); }
  50% { transform: scaleX(-1) translateY(-5px) scale(1.05, 0.95); }
}

@keyframes lunge-right {
  0% { transform: translateX(0) rotate(0deg); }
  50% { transform: translateX(120px) rotate(15deg) scale(1.1); }
  100% { transform: translateX(0) rotate(0deg); }
}
/* 反転状態からの攻撃モーション */
@keyframes lunge-left-flipped {
  0% { transform: scaleX(-1) translateX(0) rotate(0deg); }
  50% { transform: scaleX(-1) translateX(120px) rotate(15deg) scale(1.1); } /* 内部的に右へ動かして反転で見せる */
  100% { transform: scaleX(-1) translateX(0) rotate(0deg); }
}

@keyframes shake-damage {
  0% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(-10px, 0) rotate(-10deg); }
  50% { transform: translate(10px, 0) rotate(10deg); }
  75% { transform: translate(-10px, 0) rotate(-10deg); }
  100% { transform: translate(0, 0) rotate(0deg); }
}

@keyframes fly-right {
  0% { transform: translateX(0) scale(1); opacity: 1; }
  100% { transform: translateX(250px) scale(0.5); opacity: 0; }
}
@keyframes fly-left {
  0% { transform: translateX(0) scale(1); opacity: 1; }
  100% { transform: translateX(-250px) scale(0.5); opacity: 0; }
}

/* =======================================
   その他共通
   ======================================= */
.center-area { height: 80px; display: flex; justify-content: center; align-items: center; z-index: 30; }
.vs-logo { font-size: 4rem; font-weight: 900; font-style: italic; text-shadow: 0 0 20px #ff9100; }
.clash-effect { font-size: 3rem; animation: popIn 0.2s; }
.result-badge { text-align: center; animation: popUp 0.5s; }
.crown { font-size: 3rem; display: block; animation: bounce 1s infinite; }
.winner-text { font-size: 1.2rem; color: #ffd700; font-weight: bold; }
.winner-name { font-size: 1.8rem; font-weight: bold; }

.action-footer { margin-top: 10px; display: flex; gap: 10px; z-index: 30; animation: fadeIn 1s; }
button { padding: 10px 20px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s; }
button:hover { transform: translateY(-3px); }
.retry-btn { background: #ff9800; color: white; }
.home-btn { background: #03a9f4; color: white; }
.top-btn { background: #fff; color: #555; }

@keyframes popIn { from { transform: scale(0); } to { transform: scale(1); } }
@keyframes popUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>