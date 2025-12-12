<script setup>
import { computed } from 'vue'

defineProps({
  scale: {
    type: Number,
    default: 1
  }
})

// --- ユーティリティ: ランダム生成用関数 ---
const random = (min, max) => Math.random() * (max - min) + min
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
const randomPick = (arr) => arr[Math.floor(Math.random() * arr.length)]

// --- 1. 山 (自動生成: 15個) ---
const mountainColors = ['#1b5e20', '#2e7d32', '#43a047', '#689f38', '#7cb342', '#8bc34a', '#9ccc65']
const mountains = Array.from({ length: 15 }).map((_, i) => ({
  id: `m-${i}`,
  heightM: random(300, 800),
  widthM: random(500, 1200),
  color: randomPick(mountainColors),
  left: `${random(-20, 100)}%`,
  zIndex: randomInt(1, 3)
})).sort((a, b) => a.heightM - b.heightM)

// --- 3. 中景のオフィスビル (自動生成: 50個に増量) ---
// 摩天楼を消した分、こちらの数を増やし、高さのバリエーションを広げました
const midColors = ['#90a4ae', '#b0bec5', '#cfd8dc', '#78909c'] // 色味も少し濃い目を追加
const midBuildings = Array.from({ length: 150 }).map((_, i) => ({
  id: `md-${i}`,
  heightM: random(50, 250), // 高さの幅を広げました (低い雑居ビル〜そこそこのビル)
  widthM: random(30, 90),
  left: `${random(-10, 110)}%`, // 画面端までしっかり配置
  color: randomPick(midColors),
  zIndex: randomInt(4, 6) // 重なり順をランダムに
})).sort((a, b) => a.heightM - b.heightM) // 奥から手前へ並べ替え

// --- 4. 近景の住宅・商店 (自動生成: 45個) ---
const nearColors = ['#ffcc80', '#ef5350', '#81d4fa', '#fff59d', '#a5d6a7', '#ffab91', '#b39ddb', '#90caf9']
const roofColors = ['#c62828', '#fbc02d', '#388e3c', '#d84315', '#5e35b1', '#e65100', '#1565c0']
const types = ['flat', 'shop', 'house', 'house', 'flat']

const nearBuildings = Array.from({ length: 80 }).map((_, i) => {
  const type = randomPick(types)
  const baseLeft = (i / 80) * 100
  const jitter = random(-2, 2)
  
  return {
    id: `n-${i}`,
    type: type,
    heightM: type === 'flat' ? random(40, 100) : random(10, 30),
    widthM: random(20, 45),
    left: `${Math.max(0, Math.min(100, baseLeft + jitter))}%`,
    color: randomPick(nearColors),
    roof: randomPick(roofColors),
    win: randomPick(['grid', 'glass', 'normal']),
    zIndex: randomInt(10, 20)
  }
}).sort(() => Math.random() - 0.5)

</script>

<template>
  <div class="city-container">
    <div class="sky"></div>
    <div class="sun"></div>

    <div class="cloud-layer">
      <div class="cloud c1"></div>
      <div class="cloud c2"></div>
      <div class="cloud c3"></div>
    </div>

    <div class="mountain-layer">
      <svg 
        v-for="m in mountains" :key="m.id" 
        class="mountain-svg"
        viewBox="0 0 100 100" 
        preserveAspectRatio="none"
        :style="{ height: (m.heightM * scale)+'px', width: (m.widthM * scale)+'px', left: m.left, zIndex: m.zIndex }"
      >
        <path d="M0 100 L40 20 Q50 0 60 20 L100 100 Z" :fill="m.color" />
      </svg>
    </div>

    <div class="layer mid-layer">
      <div 
        v-for="b in midBuildings" :key="b.id" 
        class="building mid" 
        :style="{ 
          height: (b.heightM * scale)+'px', 
          width: (b.widthM * scale)+'px', 
          left: b.left, 
          backgroundColor: b.color,
          zIndex: b.zIndex
        }"
      ><div class="mid-windows"></div></div>
    </div>

    <div class="layer near-layer">
      <div 
        v-for="b in nearBuildings" :key="b.id" 
        class="building near" 
        :style="{ 
          height: (b.heightM * scale)+'px', 
          width: (b.widthM * scale)+'px', 
          left: b.left, 
          backgroundColor: b.color,
          zIndex: b.zIndex
        }"
      >
        <div v-if="b.type === 'house'" class="roof triangle" :style="{ borderBottomColor: b.roof, bottom: (b.heightM * scale)+'px' }"></div>
        <div v-if="b.type === 'shop'" class="roof trapezoid" :style="{ borderBottomColor: b.roof, bottom: (b.heightM * scale)+'px' }"></div>
        
        <div v-if="b.type !== 'flat'" class="door"></div>
        <div v-if="b.type === 'house'" class="window square icon-window"></div>
        <div v-if="b.type === 'shop'" class="window wide shop-window"></div>
        
        <div v-if="b.type === 'flat' && b.win === 'grid'" class="grid-windows"></div>
        <div v-if="b.type === 'flat' && b.win === 'glass'" class="glass-windows"></div>
        <div v-if="b.type === 'flat' && b.win === 'normal'" class="mid-windows"></div>
      </div>
    </div>

    <div class="ground-road"></div>
  </div>
</template>

<style scoped>
.city-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 0; }
.sky { position: absolute; top: 0; left: 0; width: 100%; height: 80%; background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 100%); z-index: 0; }

.sun {
  position: absolute;
  top: 50px; right: 50px;
  width: 80px; height: 80px;
  background: radial-gradient(circle, #ffd54f 40%, #ffca28 100%);
  border-radius: 50%;
  box-shadow: 0 0 40px rgba(255, 213, 79, 0.6), 0 0 80px rgba(255, 213, 79, 0.3);
  z-index: 0;
}

.cloud-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
.cloud {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  animation: floatCloud 60s linear infinite;
}
.cloud::after, .cloud::before {
  content: '';
  position: absolute;
  background: inherit;
  border-radius: 50%;
}

.c1 { top: 80px; left: -150px; width: 120px; height: 40px; animation-duration: 180s; }
.c1::after { width: 50px; height: 50px; top: -25px; left: 20px; }
.c1::before { width: 40px; height: 40px; top: -15px; left: 60px; }

.c2 { top: 150px; left: -100px; width: 80px; height: 30px; opacity: 0.7; animation-duration: 120s; animation-delay: -20s; }
.c2::after { width: 35px; height: 35px; top: -18px; left: 10px; }
.c2::before { width: 25px; height: 25px; top: -10px; left: 40px; }

.c3 { top: 40px; left: -120px; width: 100px; height: 35px; opacity: 0.6; animation-duration: 90s; animation-delay: -10s; }
.c3::after { width: 45px; height: 45px; top: -20px; left: 15px; }
.c3::before { width: 35px; height: 35px; top: -10px; left: 50px; }

@keyframes floatCloud {
  0% { transform: translateX(0); }
  100% { transform: translateX(120vw); }
}

.layer { position: absolute; left: 0; width: 100%; height: 100%; pointer-events: none; }
.building { position: absolute; bottom: 0; transition: all 0.5s ease-out; }

.mountain-layer { position: absolute; bottom: 25px; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; }
.mountain-svg { position: absolute; bottom: 0; transition: all 0.5s ease-out; }

/* ★修正: .far-layer, .far のスタイルを削除しました */

.mid-layer { bottom: 20px; z-index: 5; }
.mid { border: 1px solid rgba(0,0,0,0.1); border-bottom: none; }
.mid-windows { position: absolute; top: 5%; left: 10%; right: 10%; bottom: 5%; background-image: linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px); background-size: 10% 4%; background-color: #546e7a; opacity: 0.5; }

.near-layer { bottom: 15px; z-index: 8; }
.near { border: 1px solid rgba(0,0,0,0.1); border-bottom: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }

.roof { position: absolute; left: -10%; width: 120%; height: 0; border-style: solid; border-color: transparent; }
.triangle { border-width: 0 15px 20px 15px; }
.trapezoid { border-width: 0 10px 15px 10px; width: 100%; left: 0; }

.door { position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 20%; height: 30%; background: #795548; border: 1px solid #5d4037; }
.window { position: absolute; background: #e1f5fe; border: 2px solid #b3e5fc; }
.square { width: 25%; height: 25%; }
.wide { width: 60%; height: 30%; }
.icon-window { top: 20%; left: 50%; transform: translateX(-50%); }
.shop-window { top: 20%; left: 20%; }

.grid-windows { position: absolute; top: 5%; left: 10%; right: 10%; bottom: 5%; background-image: linear-gradient(#fff 2px, transparent 2px), linear-gradient(90deg, #fff 2px, transparent 2px); background-size: 15% 8%; background-color: #90a4ae; }
.glass-windows { position: absolute; top: 2%; left: 2%; right: 2%; bottom: 2%; background: linear-gradient(135deg, #b3e5fc 0%, #4fc3f7 50%, #039be5 100%); opacity: 0.8; }

.ground-road { position: absolute; bottom: 0; left: 0; width: 100%; height: 25px; z-index: 20; background: linear-gradient(to bottom, #9e9e9e 0%, #616161 100%); border-top: 3px solid #bdbdbd; }
</style>