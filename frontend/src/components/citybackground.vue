<script setup>
defineProps({
  scale: {
    type: Number,
    default: 1
  }
})

// --- 1. 山 (一番奥) ---
const mountains = [
  { id: 'm1', heightM: 400, widthM: 700, color: '#90a4ae', left: '-15%', zIndex: 1 },
  { id: 'm2', heightM: 650, widthM: 900, color: '#78909c', left: '30%',  zIndex: 2 },
  { id: 'm3', heightM: 350, widthM: 600, color: '#90a4ae', left: '75%',  zIndex: 1 },
]

// --- 2. 遠景の摩天楼 (奥) ---
const farBuildings = [
  { id: 'f1', heightM: 280, widthM: 50, left: '2%' },
  { id: 'f2', heightM: 320, widthM: 60, left: '8%' },
  { id: 'f3', heightM: 250, widthM: 45, left: '18%' },
  { id: 'f4', heightM: 350, widthM: 70, left: '25%' },
  { id: 'f5', heightM: 290, widthM: 55, left: '38%' },
  { id: 'f6', heightM: 220, widthM: 40, left: '50%' },
  { id: 'f7', heightM: 310, widthM: 65, left: '58%' },
  { id: 'f8', heightM: 260, widthM: 50, left: '72%' },
  { id: 'f9', heightM: 340, widthM: 60, left: '82%' },
  { id: 'f10', heightM: 270, widthM: 45, left: '92%' },
]

// --- 3. 中景のオフィスビル (中) ---
const midBuildings = [
  { id: 'md1', heightM: 150, widthM: 70, left: '5%',  color: '#b0bec5' },
  { id: 'md2', heightM: 180, widthM: 50, left: '15%', color: '#cfd8dc' },
  { id: 'md3', heightM: 130, widthM: 80, left: '28%', color: '#b0bec5' },
  { id: 'md4', heightM: 200, widthM: 60, left: '42%', color: '#cfd8dc' },
  { id: 'md5', heightM: 160, widthM: 75, left: '55%', color: '#b0bec5' },
  { id: 'md6', heightM: 190, widthM: 55, left: '70%', color: '#cfd8dc' },
  { id: 'md7', heightM: 140, widthM: 65, left: '85%', color: '#b0bec5' },
]

// --- 4. 近景の住宅・商店 (手前) ---
const nearBuildings = [
  { id: 'n1', type: 'flat', heightM: 80, widthM: 40, left: '3%', color: '#ffcc80', win: 'grid' },
  { id: 'n2', type: 'shop', heightM: 25, widthM: 50, left: '12%', color: '#ef5350', roof: '#c62828' },
  { id: 'n3', type: 'flat', heightM: 60, widthM: 35, left: '22%', color: '#81d4fa', win: 'glass' },
  { id: 'n4', type: 'house', heightM: 15, widthM: 25, left: '35%', color: '#fff59d', roof: '#fbc02d' },
  { id: 'n5', type: 'house', heightM: 20, widthM: 30, left: '45%', color: '#a5d6a7', roof: '#388e3c' },
  { id: 'n6', type: 'shop',  heightM: 30, widthM: 40, left: '55%', color: '#ffab91', roof: '#d84315' },
  { id: 'n7', type: 'house', heightM: 18, widthM: 28, left: '70%', color: '#b39ddb', roof: '#5e35b1' },
  { id: 'n8', type: 'flat',  heightM: 50, widthM: 30, left: '80%', color: '#90caf9', win: 'grid' },
  { id: 'n9', type: 'house', heightM: 12, widthM: 20, left: '90%', color: '#ffcc80', roof: '#e65100' },
]
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

    <div class="layer far-layer">
      <div v-for="b in farBuildings" :key="b.id" class="building far" :style="{ height: (b.heightM * scale)+'px', width: (b.widthM * scale)+'px', left: b.left }"></div>
    </div>

    <div class="layer mid-layer">
      <div v-for="b in midBuildings" :key="b.id" class="building mid" :style="{ height: (b.heightM * scale)+'px', width: (b.widthM * scale)+'px', left: b.left, backgroundColor: b.color }"><div class="mid-windows"></div></div>
    </div>

    <div class="layer near-layer">
      <div v-for="b in nearBuildings" :key="b.id" class="building near" :style="{ height: (b.heightM * scale)+'px', width: (b.widthM * scale)+'px', left: b.left, backgroundColor: b.color }">
        <div v-if="b.type === 'house'" class="roof triangle" :style="{ borderBottomColor: b.roof, bottom: (b.heightM * scale)+'px' }"></div>
        <div v-if="b.type === 'shop'" class="roof trapezoid" :style="{ borderBottomColor: b.roof, bottom: (b.heightM * scale)+'px' }"></div>
        <div v-if="b.type !== 'flat'" class="door"></div>
        <div v-if="b.type === 'house'" class="window square icon-window"></div>
        <div v-if="b.type === 'shop'" class="window wide shop-window"></div>
        <div v-if="b.win === 'grid'" class="grid-windows"></div>
        <div v-if="b.win === 'glass'" class="glass-windows"></div>
      </div>
    </div>

    <div class="ground-road"></div>
  </div>
</template>

<style scoped>
.city-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 0; }
.sky { position: absolute; top: 0; left: 0; width: 100%; height: 80%; background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 100%); z-index: 0; }

/* --- ★追加: 太陽 --- */
.sun {
  position: absolute;
  top: 50px; right: 50px;
  width: 80px; height: 80px;
  background: radial-gradient(circle, #ffd54f 40%, #ffca28 100%);
  border-radius: 50%;
  box-shadow: 0 0 40px rgba(255, 213, 79, 0.6), 0 0 80px rgba(255, 213, 79, 0.3); /* 光彩 */
  z-index: 0;
}

/* --- ★追加: 雲 --- */
.cloud-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
.cloud {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  /* 雲のアニメーション */
  animation: floatCloud 60s linear infinite;
}

/* 雲の形を作る（モコモコさせる） */
.cloud::after, .cloud::before {
  content: '';
  position: absolute;
  background: inherit;
  border-radius: 50%;
}

/* 雲1 (大きめ) */
.c1 {
  top: 80px; left: -150px; /* 画面外からスタート */
  width: 120px; height: 40px;
  animation-duration: 180s; /* 流れる速さ */
}
.c1::after { width: 50px; height: 50px; top: -25px; left: 20px; }
.c1::before { width: 40px; height: 40px; top: -15px; left: 60px; }

/* 雲2 (小さめ) */
.c2 {
  top: 150px; left: -100px;
  width: 80px; height: 30px;
  opacity: 0.7;
  animation-duration: 120s; /* 遅めに */
  animation-delay: -20s; /* 途中から開始 */
}
.c2::after { width: 35px; height: 35px; top: -18px; left: 10px; }
.c2::before { width: 25px; height: 25px; top: -10px; left: 40px; }

/* 雲3 */
.c3 {
  top: 40px; left: -120px;
  width: 100px; height: 35px;
  opacity: 0.6;
  animation-duration: 80s; /* 速めに */
  animation-delay: -10s;
}
.c3::after { width: 45px; height: 45px; top: -20px; left: 15px; }
.c3::before { width: 35px; height: 35px; top: -10px; left: 50px; }

/* 雲のアニメーション定義: 画面左から右へ流れる */
@keyframes floatCloud {
  0% { transform: translateX(0); }
  100% { transform: translateX(120vw); } /* 画面幅より少し広く移動 */
}

/* --- レイヤー共通 --- */
.layer { position: absolute; left: 0; width: 100%; height: 100%; pointer-events: none; }
.building { position: absolute; bottom: 0; transition: all 0.5s ease-out; }

/* --- 山 (SVG) --- */
.mountain-layer { position: absolute; bottom: 25px; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; }
.mountain-svg { position: absolute; bottom: 0; transition: all 0.5s ease-out; }

/* --- 以下、ビルのスタイルは変更なし --- */
.far-layer { bottom: 25px; z-index: 3; }
.far { background-color: #90a4ae; border: 1px solid #78909c; border-bottom: none; opacity: 0.9; }

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