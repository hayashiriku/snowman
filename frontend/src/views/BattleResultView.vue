<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// 共通コンポーネント
import SnowEffect from '../components/Snoweffect.vue'
import OceanBackground from '../components/oceanbackground.vue'
import snowmanImg from '/public/snowman.svg'

const route = useRoute()
const router = useRouter()

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

// HP (スケーリング後の整数値)
const p1Hp = ref(0)
const p2Hp = ref(0)
const p1MaxHp = ref(1) 
const p2MaxHp = ref(1)

// 実体積（データ保持用）
const p1RealVolume = ref(0)
const p2RealVolume = ref(0)

// アニメーション管理
const p1Action = ref('idle')
const p2Action = ref('idle')
const logMessage = ref('データを取得中...') 

// ★追加: 決定した武器情報
const p1Weapon = ref(null)
const p2Weapon = ref(null)

// 武器名ポップアップ用 (攻撃時のみ表示)
const currentWeaponNameP1 = ref('')
const currentWeaponNameP2 = ref('')

// ==========================================
// 武器リスト
// ==========================================
const weaponList = [
  { name: '人参の鼻', power: 10, icon: '🥕' },
  { name: '素手', power: 50, icon: '✊' },
  { name: '雪玉', power: 150, icon: '❄️' },
  { name: 'バケツ', power: 200, icon: '🪣' },
  { name: 'つらら', power: 300, icon: '🗡️' },
  { name: 'スコップ', power: 500, icon: '🥄' },
  { name: 'スノーダンプ', power: 1000, icon: '🚜' },
  { name: '除雪車', power: 2500, icon: '🚛' },
  { name: '雪崩', power: 5000, icon: '🏔️' },
  { name: '氷河期', power: 9999, icon: '🥶' }
]

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

  // ★ここで武器を決定して固定！
  p1Weapon.value = weaponList[Math.floor(Math.random() * weaponList.length)]
  p2Weapon.value = weaponList[Math.floor(Math.random() * weaponList.length)]
  
  logMessage.value = `1P:${p1Weapon.value.name} vs 2P:${p2Weapon.value.name}`
  await sleep(1500) // 武器決定のログを見せる時間

  battleState.value = 'fighting'
  logMessage.value = 'BATTLE START!'

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

// 攻撃ロジック (固定された武器を使用)
const performAttack = async (attacker) => {
  
  // 決定済みの武器を取得
  const weapon = attacker === 1 ? p1Weapon.value : p2Weapon.value

  // モーションと名前ポップアップ表示
  if (attacker === 1) {
    p1Action.value = 'attack'
    currentWeaponNameP1.value = weapon.name
  } else {
    p2Action.value = 'attack'
    currentWeaponNameP2.value = weapon.name
  }

  await sleep(300) 

  // ダメージ計算 (固定攻撃力ベース)
  const variation = 0.9 + Math.random() * 0.2
  const damage = Math.floor(weapon.power * variation)

  if (attacker === 1) {
    p2Action.value = 'damage'
    p2Hp.value = Math.max(0, p2Hp.value - damage)
    logMessage.value = `先攻の攻撃！ ${damage}ダメージ`
  } else {
    p1Action.value = 'damage'
    p1Hp.value = Math.max(0, p1Hp.value - damage)
    logMessage.value = `後攻の攻撃！ ${damage}ダメージ`
  }

  await sleep(600)
  p1Action.value = 'idle'
  p2Action.value = 'idle'
  currentWeaponNameP1.value = ''
  currentWeaponNameP2.value = ''
}

const finishBattle = () => {
  battleState.value = 'finished'
  if (p1Hp.value <= 0 && p2Hp.value <= 0) {
    winner.value = 2 
    logMessage.value = '相打ち（引き分け）'
  } else {
    winner.value = p1Hp.value > 0 ? 1 : 2
    logMessage.value = winner.value === 1 ? '先攻(赤)の完全勝利！' : '後攻(青)の完全勝利！'
  }
}

const getBadgeInfo = (label) => {
  const type = detectType(label)
  if (type === 'day') return { text: '1 Day', color: '#4caf50' }
  if (type === 'month') return { text: '1 Month', color: '#ff9800' }
  return { text: '1 Year', color: '#f44336' }
}

const getScale = (battleHp) => {
  if (battleHp <= 0) return 0.5
  const logVal = Math.log10(battleHp)
  const scale = 0.6 + (Math.max(0, logVal - 3) * 0.15)
  return Math.min(2.0, Math.max(0.6, scale))
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
        <div class="hp-bar-fill red" :style="{ width: (p1Hp / p1MaxHp * 100) + '%' }"></div>
      </div>
      
      <div class="status-text">
        <span class="hp-label">HP:</span>
        <span class="hp-value">{{ p1Hp.toLocaleString() }}</span>
      </div>
      
      <div class="avatar-wrapper">
        <div v-if="p1Action === 'attack'" class="weapon-popup red-pop">
          {{ currentWeaponNameP1 }}
        </div>

        <img 
          :src="snowmanImg" 
          class="snowman-img red-tint" 
          :class="p1Action"
          :style="{ transform: `scale(${getScale(p1MaxHp)})` }" 
        />

        <div v-if="p1Weapon" class="equipped-weapon p1-weapon">
          {{ p1Weapon.icon }}
        </div>
      </div>

      <div class="info-box">
        <h2 class="pref-name">{{ p1Data.name }}</h2>
        <p class="date-text">{{ p1Data.label }}</p>
        <span class="type-badge" :style="{ background: getBadgeInfo(p1Data.label).color }">
          {{ getBadgeInfo(p1Data.label).text }}
        </span>
      </div>
    </div>

    <div class="center-area">
      <div v-if="battleState === 'ready'" class="vs-logo">VS</div>
      <div v-else-if="battleState === 'fighting'" class="clash-effect">⚔️</div>
      <div v-else-if="battleState === 'finished'" class="result-badge">
        <div class="crown">👑</div>
        <div class="winner-text">WINNER</div>
      </div>
    </div>

    <div class="player-panel p2" :class="{ 'loser': battleState === 'finished' && winner === 1 }">
      <div class="hp-bar-container">
        <div class="hp-bar-fill blue" :style="{ width: (p2Hp / p2MaxHp * 100) + '%' }"></div>
      </div>
      
      <div class="status-text">
        <span class="hp-label">HP:</span>
        <span class="hp-value">{{ p2Hp.toLocaleString() }}</span>
      </div>

      <div class="avatar-wrapper">
        <div v-if="p2Action === 'attack'" class="weapon-popup blue-pop">
          {{ currentWeaponNameP2 }}
        </div>

        <img 
          :src="snowmanImg" 
          class="snowman-img blue-tint flipped" 
          :class="p2Action" 
          :style="{ transform: `scaleX(-1) scale(${getScale(p2MaxHp)})` }"
        />

        <div v-if="p2Weapon" class="equipped-weapon p2-weapon">
          {{ p2Weapon.icon }}
        </div>
      </div>

      <div class="info-box">
        <h2 class="pref-name">{{ p2Data.name }}</h2>
        <p class="date-text">{{ p2Data.label }}</p>
        <span class="type-badge" :style="{ background: getBadgeInfo(p2Data.label).color }">
          {{ getBadgeInfo(p2Data.label).text }}
        </span>
      </div>
    </div>

    <div class="battle-log">{{ logMessage }}</div>

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
  border-radius: 20px; padding: 40px 15px 15px 15px;
  margin: 15px 0;
  display: flex; align-items: center; color: #333;
  transition: all 0.5s;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  z-index: 20;
}
.player-panel.loser { filter: grayscale(100%) brightness(0.6); transform: scale(0.9); opacity: 0.8; }
.p1 { border-bottom: 5px solid #ff5252; }
.p2 { border-bottom: 5px solid #448aff; flex-direction: row-reverse; text-align: right; }

.info-box { flex: 1; padding: 0 15px; }
.pref-name { margin: 0; font-size: 1.6rem; color: #222; }
.date-text { margin: 0; font-weight: bold; color: #555; font-size: 0.9rem; }
.type-badge { 
  display: inline-block; color: #fff; 
  font-size: 0.7rem; padding: 3px 8px; border-radius: 4px; margin-top: 5px; 
  font-weight: bold;
}

/* =======================================
   HP & 体積表示
   ======================================= */
.hp-bar-container {
  position: absolute; top: -12px; left: 10px; right: 10px; height: 12px;
  background: #444; border-radius: 10px; overflow: hidden;
  border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
.hp-bar-fill { height: 100%; transition: width 0.3s ease-out; }
.red { background: #ff1744; }
.blue { background: #2979ff; }

.status-text {
  position: absolute; top: -45px; right: 10px;
  color: #fff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);
  text-align: right; line-height: 1.2;
}
.p1 .status-text { left: 10px; right: auto; text-align: left; }

.hp-label { font-size: 0.9rem; font-weight: bold; margin-right: 5px; color: #ffeb3b; }
.hp-value { font-size: 1.5rem; font-weight: 900; color: #fff; }

/* =======================================
   雪だるま画像 & 武器表示
   ======================================= */
.avatar-wrapper {
  position: relative; width: 100px; height: 100px;
  display: flex; justify-content: center; align-items: center; overflow: visible; 
}
.snowman-img {
  width: 100%; height: 100%; object-fit: contain;
  animation: idle-bounce 1.5s infinite ease-in-out; transform-origin: center bottom;
  transition: transform 0.3s; 
}
.red-tint { filter: drop-shadow(0 0 8px rgba(255, 0, 0, 0.8)); }
.blue-tint { filter: drop-shadow(0 0 8px rgba(0, 80, 255, 0.8)); }
.flipped { transform: scaleX(-1); }
.flipped.idle { animation: idle-bounce-flipped 1.5s infinite ease-in-out; }

.p1 .snowman-img.attack { animation: lunge-right 0.3s forwards; }
.p2 .snowman-img.attack { animation: lunge-left-flipped 0.3s forwards; }
.damage {
  animation: shake-damage 0.4s forwards !important;
  filter: sepia(100%) saturate(1000%) hue-rotate(-50deg) !important;
}

/* 武器名ポップアップ */
.weapon-popup {
  position: absolute; top: -35px; left: 50%; transform: translateX(-50%);
  font-weight: bold; font-size: 1.1rem; color: #fff; white-space: nowrap;
  padding: 5px 12px; border-radius: 12px;
  animation: popUpFade 0.5s ease-out forwards;
  z-index: 40; border: 2px solid #fff;
}
.red-pop { background: #ff5252; box-shadow: 0 4px 10px rgba(255, 0, 0, 0.4); }
.blue-pop { background: #448aff; box-shadow: 0 4px 10px rgba(0, 0, 255, 0.4); }

/* ★装備武器アイコンのスタイル */
.equipped-weapon {
  position: absolute;
  font-size: 2rem;
  z-index: 35;
  filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3));
  animation: floatWeapon 2s ease-in-out infinite;
}
.p1-weapon { bottom: -10px; right: -10px; } /* 1Pは右下 */
.p2-weapon { bottom: -10px; left: -10px; }  /* 2Pは左下 */

/* =======================================
   その他共通
   ======================================= */
.center-area { height: 60px; display: flex; justify-content: center; align-items: center; z-index: 30; }
.vs-logo { font-size: 4rem; font-weight: 900; font-style: italic; text-shadow: 0 0 20px #ff9100; }
.clash-effect { font-size: 3rem; animation: popIn 0.2s; }
.result-badge { text-align: center; animation: popUp 0.5s; }
.crown { font-size: 3rem; display: block; animation: bounce 1s infinite; }
.winner-text { font-size: 1.2rem; color: #ffd700; font-weight: bold; }

.battle-log {
  margin-top: 10px; height: 30px;
  font-weight: bold; font-size: 1.1rem; color: #fff; text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  animation: fadeIn 0.2s;
  white-space: nowrap; 
}

.action-footer { margin-top: 15px; display: flex; gap: 10px; z-index: 30; animation: fadeIn 1s; }
button { padding: 10px 20px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s; }
button:hover { transform: translateY(-3px); }
.retry-btn { background: #ff9800; color: white; }
.home-btn { background: #03a9f4; color: white; }
.top-btn { background: #fff; color: #555; }

/* Keyframes */
@keyframes idle-bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
@keyframes idle-bounce-flipped { 0%, 100% { transform: scaleX(-1) translateY(0); } 50% { transform: scaleX(-1) translateY(-5px); } }
@keyframes lunge-right { 0% { transform: translateX(0); } 50% { transform: translateX(120px) rotate(15deg); } 100% { transform: translateX(0); } }
@keyframes lunge-left-flipped { 0% { transform: scaleX(-1) translateX(0); } 50% { transform: scaleX(-1) translateX(120px) rotate(15deg); } 100% { transform: scaleX(-1) translateX(0); } }
@keyframes shake-damage { 0% { transform: translate(0); } 25% { transform: translate(-10px, 0); } 50% { transform: translate(10px, 0); } 75% { transform: translate(-10px, 0); } 100% { transform: translate(0); } }
@keyframes popIn { from { transform: scale(0); } to { transform: scale(1); } }
@keyframes popUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes popUpFade { 0% { transform: translateX(-50%) translateY(10px); opacity: 0; } 100% { transform: translateX(-50%) translateY(0); opacity: 1; } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* 武器アイコンのふわふわアニメーション */
@keyframes floatWeapon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>