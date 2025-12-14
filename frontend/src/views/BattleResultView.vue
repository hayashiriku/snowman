<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// 共通コンポーネント
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'
import snowmanImg from '/snowman.svg'

const route = useRoute()
const router = useRouter()

// ★ BGMプレイヤーの参照
const bgmPlayer = ref(null)

// パラメータ取得
const p1Data = computed(() => ({
  name: route.query.p1_name || 'Player 1',
  label: route.query.p1_label || '日付不明',
  dateRaw: route.query.p1_date || '2024-01-01',
  id: Number(route.query.p1_id) || 1
}))

const p2Data = computed(() => ({
  name: route.query.p2_name || 'Player 2',
  label: route.query.p2_label || '日付不明',
  dateRaw: route.query.p2_date || '2024-01-01',
  id: Number(route.query.p2_id) || 13
}))

// バトル状態管理
const battleState = ref('ready') 
const winner = ref(null)
const introStep = ref(0) // 0:なし, 1:READY, 2:FIGHT

// HP
const p1Hp = ref(0)
const p2Hp = ref(0)
const p1MaxHp = ref(1) 
const p2MaxHp = ref(1)

// 実体積
const p1RealVolume = ref(0)
const p2RealVolume = ref(0)

// アニメーション管理
const p1Action = ref('idle')
const p2Action = ref('idle')
const logMessage = ref('データを取得中...') 

// 決定した武器情報
const p1Weapon = ref(null)
const p2Weapon = ref(null)

// 武器名ポップアップ
const currentWeaponNameP1 = ref('')
const currentWeaponNameP2 = ref('')

// ==========================================
// 武器リスト (SFXパスを追加)
// ※パスは public フォルダからの絶対パスにしています
// ==========================================
const weaponList = [
  { name: '弓', power: 1000, icon: '/weapon/311747.svg', sfx: '/BGM/47042.mp3' },
  { name: '三叉槍', power: 300, icon: '/weapon/151565.svg', sfx: '/BGM/151565.mp3' },
  { name: '手裏剣', power: 500, icon: '/weapon/153172.svg', sfx: '/BGM/153172.mp3' },
  { name: '剣', power: 1500, icon: '/weapon/310793.svg', sfx: '/BGM/310793.mp3' },
  { name: 'ライフル', power: 3000, icon: '/weapon/308095.svg', sfx: '/BGM/308095.mp3' } 
]

// ==========================================
// 効果音再生機能 (ワンショット再生用)
// ==========================================
const playSe = (path, timeLimitSec = null) => {
  if (!path) return null;
  try {
    const audio = new Audio()
    audio.volume = 0.5 

    audio.onloadedmetadata = () => {
      const duration = audio.duration 
      if (timeLimitSec && duration > timeLimitSec) {
        audio.playbackRate = duration / timeLimitSec
      }
      audio.play().catch(e => console.warn('SE再生エラー:', e))
    }
    audio.src = path
    return audio
  } catch (e) {
    console.error('Audio error:', e)
    return null
  }
}

const detectType = (label) => {
  if (label.includes('日')) return 'day'
  if (label.includes('月')) return 'month'
  return 'year'
}

// API連携
const fetchSnowData = async (playerData) => {
  try {
    const type = detectType(playerData.label)
    const res = await fetch('http://localhost:8000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prefecture_id: playerData.id,
        target_date: playerData.dateRaw,
        period_type: type
      })
    })

    if (res.ok) {
      const data = await res.json()
      const rawVolume = data.volume_m3 
      let divisor = 100000 
      if (type === 'month') divisor = 1500000
      else if (type === 'year') divisor = 5000000
      const battleHp = Math.floor(rawVolume / divisor)
      return {
        rawVolume: Math.floor(rawVolume), 
        battleHp: Math.max(50, battleHp) 
      }
    } else {
      console.error('API Error:', await res.text())
      return { rawVolume: 0, battleHp: 100 }
    }
  } catch (e) {
    console.error('Connection Error:', e)
    return { rawVolume: 0, battleHp: 100 }
  }
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const startBattleSequence = async () => {
  const [res1, res2] = await Promise.all([
    fetchSnowData(p1Data.value),
    fetchSnowData(p2Data.value)
  ])

  // HP設定
  p1RealVolume.value = res1.rawVolume
  p1MaxHp.value = res1.battleHp
  p1Hp.value = res1.battleHp
  
  p2RealVolume.value = res2.rawVolume
  p2MaxHp.value = res2.battleHp
  p2Hp.value = res2.battleHp

  await sleep(500)

  // HPチェック
  if (p1Hp.value <= 10 && p2Hp.value <= 10) {
    logMessage.value = '雪が足りず勝負になりません...'
    finishBattle()
    return
  }

  // 武器を決定
  p1Weapon.value = weaponList[Math.floor(Math.random() * weaponList.length)]
  p2Weapon.value = weaponList[Math.floor(Math.random() * weaponList.length)]
  
  logMessage.value = `武器決定！ ${p1Weapon.value.name} vs ${p2Weapon.value.name}`
  await sleep(2000) 

  // Ready... FIGHT! 演出
  logMessage.value = '' 
  introStep.value = 1 // READY
  await sleep(1500) 

  introStep.value = 2 // FIGHT!
  
  // FIGHT音声 (1秒に短縮再生)
  playSe('/BGM/bell.mp3', 1.0)
  
  await sleep(1000) 
  
  introStep.value = 0 // 演出終了
  battleState.value = 'fighting'
  logMessage.value = 'BATTLE START!'

  // ★ BGM再生開始
  if (bgmPlayer.value) {
    bgmPlayer.value.volume = 0.3 // BGMは少し控えめ
    bgmPlayer.value.play().catch(e => console.warn('BGM Auto-play blocked', e))
  }

  // バトルループ
  while (p1Hp.value > 0 && p2Hp.value > 0) {
    const isP1Turn = Math.random() > 0.5
    if (isP1Turn) {
      await performAttack(1)
    } else {
      await performAttack(2)
    }
    await sleep(1000)
  }
  finishBattle()
}

// 攻撃ロジック
const performAttack = async (attacker) => {
  const weapon = attacker === 1 ? p1Weapon.value : p2Weapon.value

  if (attacker === 1) {
    p1Action.value = 'attack'
    currentWeaponNameP1.value = weapon.name
  } else {
    p2Action.value = 'attack'
    currentWeaponNameP2.value = weapon.name
  }

  await sleep(300) 

  // ★ 武器の効果音再生
  if (weapon.sfx) {
    playSe(weapon.sfx)
  }

  const damage = weapon.power

  if (attacker === 1) {
    p2Action.value = 'damage'
    p2Hp.value = Math.max(0, p2Hp.value - damage)
    logMessage.value = `${p1Data.value.name}が${weapon.name}で攻撃！ ${damage}ダメージ！`
  } else {
    p1Action.value = 'damage'
    p1Hp.value = Math.max(0, p1Hp.value - damage)
    logMessage.value = `${p2Data.value.name}が${weapon.name}で攻撃！ ${damage}ダメージ！`
  }

  await sleep(600)
  p1Action.value = 'idle'
  p2Action.value = 'idle'
  currentWeaponNameP1.value = ''
  currentWeaponNameP2.value = ''
}

const finishBattle = () => {
  battleState.value = 'finished'

  // ★ BGM停止
  if (bgmPlayer.value) {
    bgmPlayer.value.pause()
    bgmPlayer.value.currentTime = 0
  }
  
  // 結果発表音
  playSe('/BGM/fanfare.mp3')

  if (p1Hp.value <= 0 && p2Hp.value <= 0) {
    winner.value = 0 // 引き分け
    logMessage.value = '勝負あり！'
  } else {
    winner.value = p1Hp.value > 0 ? 1 : 2
    logMessage.value = '勝負あり！'
  }
}

// スケール計算
const getScale = (battleHp) => {
  if (battleHp <= 0) return 0.5
  const logVal = Math.log10(battleHp)
  const scale = 1.0 + (Math.max(0, logVal - 3) * 0.05) 
  return Math.min(1.5, Math.max(1.0, scale)) 
}

const p1HpPercent = computed(() => Math.max(0, p1Hp.value / p1MaxHp.value * 100))
const p2HpPercent = computed(() => Math.max(0, p2Hp.value / p2MaxHp.value * 100))

onMounted(() => {
  startBattleSequence()
})

const goBackBattle = () => router.push('/battle')
const goTop = () => router.push('/')
</script>

<template>
  <SnowEffect />

  <audio ref="bgmPlayer" src="/BGM/BattleBGM.mp3" loop hidden></audio>
  
  <div class="battle-result-container">
    <OceanBackground />

    <div class="header-status-bar">
      <div class="player-status-block p1-block">
        <div class="info-text">
          <h2 class="pref-name">{{ p1Data.name }}</h2>
          <p class="date-text">{{ p1Data.label }}</p>
          <span class="hp-value-label">HP: {{ p1Hp.toLocaleString() }}</span>
        </div>
        <div class="hp-bar-container">
          <div class="hp-bar-fill red" :style="{ width: p1HpPercent + '%' }"></div>
        </div>
      </div>

      <div class="ko-logo">
        <div class="ko-text">
          <span v-if="battleState === 'finished'">K.O.</span>
          <span v-else-if="battleState === 'fighting'">FIGHT!</span>
          <span v-else>VS</span>
        </div>
      </div>

      <div class="player-status-block p2-block">
        <div class="info-text">
          <h2 class="pref-name">{{ p2Data.name }}</h2>
          <p class="date-text">{{ p2Data.label }}</p>
          <span class="hp-value-label">HP: {{ p2Hp.toLocaleString() }}</span>
        </div>
        <div class="hp-bar-container">
          <div class="hp-bar-fill blue" :style="{ width: p2HpPercent + '%' }"></div>
        </div>
      </div>
    </div>

    <div class="avatar-stage">
      <div class="player-avatar-area p1" :class="{ 'loser-shake': battleState === 'finished' && winner === 2 }">
        <div v-if="p1Action === 'attack'" class="weapon-popup red-pop">
          {{ currentWeaponNameP1 }}
        </div>

        <img 
          :src="snowmanImg" 
          class="snowman-img red-tint" 
          :class="p1Action"
          :style="{ transform: `scale(${getScale(p1MaxHp)})` }" 
        />
        
        <img v-if="p1Weapon" :src="p1Weapon.icon" class="equipped-weapon p1-weapon-icon" alt="Player 1 Weapon" />
      </div>

      <div class="player-avatar-area p2" :class="{ 'loser-shake': battleState === 'finished' && winner === 1 }">
        <div v-if="p2Action === 'attack'" class="weapon-popup blue-pop">
          {{ currentWeaponNameP2 }}
        </div>

        <img 
          :src="snowmanImg" 
          class="snowman-img blue-tint flipped" 
          :class="p2Action" 
          :style="{ transform: `scaleX(-1) scale(${getScale(p2MaxHp)})` }"
        />

        <img v-if="p2Weapon" :src="p2Weapon.icon" class="equipped-weapon p2-weapon-icon" alt="Player 2 Weapon" />
      </div>
    </div>

    <div class="log-area-container">
      <div class="battle-log-box">
        <p class="log-message">▶ {{ logMessage }}</p>
      </div>
    </div>

    <div v-if="introStep > 0" class="intro-overlay">
      <div v-if="introStep === 1" class="intro-text ready-anim">
        READY...
      </div>
      <div v-if="introStep === 2" class="intro-text fight-anim">
        FIGHT!
      </div>
    </div>

    <div v-if="battleState === 'finished'" class="result-overlay">
      <div class="result-card" :class="{'winner-red': winner === 1, 'winner-blue': winner === 2, 'draw-gray': winner === 0}">
        
        <div class="result-header">
          <span v-if="winner === 0">DRAW</span>
          <span v-else>WINNER!</span>
        </div>
        
        <div v-if="winner !== 0" class="crow-container">
          <span class="crow-icon">👑</span>
        </div>

        <div class="result-content">
           <div v-if="winner === 1">
             <div class="winner-name">{{ p1Data.name }}</div>
             <p class="winner-date">{{ p1Data.label }}</p>
           </div>
           <div v-else-if="winner === 2">
             <div class="winner-name">{{ p2Data.name }}</div>
             <p class="winner-date">{{ p2Data.label }}</p>
           </div>
           <div v-else class="winner-name">引き分け</div>
        </div>

        <div class="result-actions">
          <button @click="goBackBattle" class="retry-btn">⚔️ 再戦する</button>
          <button @click="goTop" class="top-btn">🏠 TOP</button>
        </div>
      </div>
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
  display: flex; flex-direction: column; justify-content: flex-start; 
  align-items: center;
  z-index: 10; overflow: hidden; color: #fff;
  padding-top: 100px; 
  padding-bottom: 50px;
}

/* =======================================
   HP & ステータスバー
   ======================================= */
.header-status-bar {
  position: fixed; top: 0; left: 0; width: 100%; height: 100px;
  background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(5px);
  display: flex; justify-content: center; align-items: center;
  padding: 10px 20px; box-sizing: border-box;
  z-index: 100;
  box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}

.player-status-block {
  flex: 1; max-width: 400px; height: 100%;
  display: flex; flex-direction: column; justify-content: center;
}
.p1-block { align-items: flex-start; }
.p2-block { align-items: flex-end; }

.info-text {
  width: 100%; padding: 0 10px; margin-bottom: 5px;
}
.p1-block .info-text { text-align: left; }
.p2-block .info-text { text-align: right; }

.pref-name { 
  margin: 0; font-size: 1.5rem; font-weight: 900; 
  text-shadow: 1px 1px 3px #000; letter-spacing: 1px;
}
.date-text { 
  margin: 0; font-size: 0.8rem; font-weight: bold; 
  color: #ffeb3b; text-shadow: 1px 1px 2px #000;
}
.hp-value-label {
  font-size: 0.9rem; font-weight: bold;
  color: #fff; text-shadow: 1px 1px 2px #000;
}

.hp-bar-container {
  width: 100%; height: 25px;
  background: #444; border-radius: 5px; overflow: hidden;
  border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.5); flex: 0 0 10px; height: 25px; max-height: 25px;
}
.hp-bar-fill { height: 100%; transition: width 0.3s ease-out; }
.red { background: linear-gradient(to right, #ff5252, #d50000); }
.blue { background: linear-gradient(to left, #448aff, #2962ff); }
.p1-block .hp-bar-container { border-right: none; }
.p2-block .hp-bar-container { border-left: none; }

.ko-logo {
  position: relative; width: 80px; height: 80px; margin: 0 10px;
  display: flex; justify-content: center; align-items: center;
  background: #ffcc00; border-radius: 50%;
  border: 5px solid #fff; box-shadow: 0 0 15px rgba(255, 255, 0, 0.8);
  font-weight: 900; color: #d50000; font-style: italic;
  transform: rotate(-10deg); z-index: 110;
}
.ko-text { font-size: 1.8rem; text-shadow: 1px 1px 2px #000; }

/* =======================================
   アバターエリア
   ======================================= */
.avatar-stage {
  flex: 1; width: 100%;
  display: flex; justify-content: space-around;
  align-items: flex-end; 
  padding-bottom: 0px; 
  box-sizing: border-box; overflow: hidden;
}

.player-avatar-area {
  position: relative; width: 45%; max-width: 300px;
  height: auto;
  display: flex; justify-content: center; align-items: flex-end;
  transition: filter 0.5s, transform 0.5s;
}

.loser-shake {
  animation: shake-loser 1s forwards infinite;
  opacity: 0.5; filter: grayscale(80%);
}

.snowman-img {
  width: 100%; height: auto; object-fit: contain;
  animation: idle-bounce 1.5s infinite ease-in-out; 
  transform-origin: center bottom;
  transition: transform 0.3s, filter 0.3s; 
  position: relative; z-index: 20;
}

.red-tint { filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.5)); }
.blue-tint { filter: drop-shadow(0 0 10px rgba(0, 80, 255, 0.5)); }
.flipped { transform: scaleX(-1); }
.flipped.idle { animation: idle-bounce-flipped 1.5s infinite ease-in-out; }

.p1 .snowman-img.attack { animation: lunge-right 0.3s forwards; }
.p2 .snowman-img.attack { animation: lunge-left-flipped 0.3s forwards; }
.damage {
  animation: shake-damage 0.4s forwards, damage-flash 0.6s ease-out forwards !important;
}

.weapon-popup {
  position: absolute; top: -50px; left: 50%; transform: translateX(-50%);
  font-weight: bold; font-size: 1.2rem; color: #fff; white-space: nowrap;
  padding: 5px 15px; border-radius: 15px;
  animation: popUpFade 0.5s ease-out forwards;
  z-index: 40; border: 3px solid #fff;
}
.red-pop { background: #ff5252; box-shadow: 0 4px 10px rgba(255, 0, 0, 0.6); }
.blue-pop { background: #448aff; box-shadow: 0 4px 10px rgba(0, 0, 255, 0.6); }

.equipped-weapon {
  position: absolute; width: 120px; height: 100px;
  object-fit: contain; z-index: 30;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));
  animation: floatWeapon 2s ease-in-out infinite;
}
.p1-weapon-icon { right: -1.5%; bottom: 175px; transform: rotate(15deg); } 
.p2-weapon-icon { left: -1.5%; bottom: 175px; transform: scaleX(-1) rotate(-15deg); } 

/* =======================================
   ログエリア
   ======================================= */
.log-area-container {
  position: absolute; bottom: 30px; 
  width: 90%; max-width: 600px;
  z-index: 50; display: flex; justify-content: center;
}
.battle-log-box {
  background: rgba(0, 0, 0, 0.7); border: 3px solid #ffcc00;
  padding: 10px 20px; border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
  min-height: 40px; text-align: left;
}
.log-message {
  margin: 0; font-weight: bold; font-size: 1.1rem; color: #fff; text-shadow: 0 1px 2px #000;
}

/* =======================================
   READY... FIGHT! 演出
   ======================================= */
.intro-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.3); /* 少し暗くする */
  display: flex; justify-content: center; align-items: center;
  z-index: 300; pointer-events: none;
}

.intro-text {
  font-family: 'Arial Black', sans-serif;
  font-style: italic;
  font-weight: 900;
  color: #ffcc00;
  text-shadow: 5px 5px 0 #d50000, -2px -2px 0 #fff;
  text-transform: uppercase;
  white-space: nowrap;
}

/* READY: 横からスライドイン & フェードイン */
.ready-anim {
  font-size: 5rem;
  animation: slideInReady 1s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

/* FIGHT: 画面奥から手前にドーン！ */
.fight-anim {
  font-size: 8rem;
  color: #ff5252;
  text-shadow: 5px 5px 0 #ffcc00, -3px -3px 0 #fff;
  animation: zoomImpact 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

@keyframes slideInReady {
  0% { transform: translateX(-100vw) skewX(-20deg); opacity: 0; }
  60% { transform: translateX(0) skewX(0deg); opacity: 1; }
  80% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes zoomImpact {
  0% { transform: scale(5); opacity: 0; }
  50% { transform: scale(1); opacity: 1; }
  70% { transform: scale(1.2) rotate(5deg); }
  100% { transform: scale(1) rotate(0deg); }
}


/* =======================================
   結果ポップアップ (Modal)
   ======================================= */
.result-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex; justify-content: center; align-items: center;
  z-index: 200;
  animation: fadeIn 0.3s ease-out;
}

.result-card {
  width: 90%; max-width: 400px;
  background: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  border: 5px solid #fff;
  transform: scale(0.5);
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  display: flex; flex-direction: column; 
}

/* 勝者に応じたテーマカラー */
.winner-red {
  background: linear-gradient(135deg, #d32f2f, #ff5252);
  border-color: #ff8a80;
}
.winner-blue {
  background: linear-gradient(135deg, #1976d2, #448aff);
  border-color: #82b1ff;
}
.draw-gray {
  background: linear-gradient(135deg, #616161, #9e9e9e);
  border-color: #bdbdbd;
}

.result-header {
  font-size: 2.5rem; font-weight: 900; font-style: italic;
  color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,0.2);
  line-height: 1;
  margin-bottom: 10px;
}

.crow-container { margin-bottom: 15px; }
.crow-icon {
  font-size: 4rem; display: inline-block;
  animation: bounceIcon 1s infinite alternate ease-in-out;
}

.result-content {
  background: rgba(255,255,255,0.2);
  padding: 20px; border-radius: 15px;
  margin-bottom: 25px;
}

.winner-name {
  font-size: 2rem; font-weight: bold; color: #fff;
  text-shadow: 0 2px 5px rgba(0,0,0,0.3);
  margin-bottom: 5px;
}

.winner-date {
  margin: 0; font-size: 1.1rem; font-weight: bold;
  color: #ffeb3b; text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

.result-actions {
  display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;
}

button { 
  padding: 15px 25px; font-size: 1rem; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s; 
}
button:hover { transform: translateY(-3px); }
.retry-btn { background: #ffca28; color: #3e2723; }
.top-btn { background: #fff; color: #555; }


/* Keyframes (既存) */
@keyframes idle-bounce { 0%, 100% { transform: scale(var(--scale, 1.0)) translateY(0); } 50% { transform: scale(var(--scale, 1.0)) translateY(-5px); } }
@keyframes idle-bounce-flipped { 0%, 100% { transform: scaleX(-1) scale(var(--scale, 1.0)) translateY(0); } 50% { transform: scaleX(-1) scale(var(--scale, 1.0)) translateY(-5px); } }
@keyframes lunge-right { 0% { transform: scale(var(--scale, 1.0)) translateX(0); } 50% { transform: scale(var(--scale, 1.0)) translateX(80px) rotate(5deg); } 100% { transform: scale(var(--scale, 1.0)) translateX(0); } }
@keyframes lunge-left-flipped { 0% { transform: scaleX(-1) scale(var(--scale, 1.0)) translateX(0); } 50% { transform: scaleX(-1) scale(var(--scale, 1.0)) translateX(80px) rotate(-5deg); } 100% { transform: scaleX(-1) scale(var(--scale, 1.0)) translateX(0); } }
@keyframes shake-damage { 0% { transform: translate(0); } 25% { transform: translate(-10px, 0); } 50% { transform: translate(10px, 0); } 75% { transform: translate(-10px, 0); } 100% { transform: translate(0); } }
@keyframes shake-loser { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(-1deg); } 75% { transform: rotate(1deg); } }
@keyframes popUpFade { 0% { opacity: 0; transform: translateX(-50%) translateY(10px); } 100% { opacity: 1; transform: translateX(-50%) translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes floatWeapon { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
@keyframes damage-flash { 0% { filter: sepia(100%) saturate(1000%) hue-rotate(-50deg) drop-shadow(0 0 10px red); } 100% { filter: none; } }
@keyframes popIn { 0% { transform: scale(0); opacity: 0; } 60% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }
@keyframes bounceIcon { 0% { transform: translateY(0); } 100% { transform: translateY(-15px); } }

.snowman-img { --scale: v-bind('getScale(p1MaxHp)'); }
.p2 .snowman-img { --scale: v-bind('getScale(p2MaxHp)'); }
</style>