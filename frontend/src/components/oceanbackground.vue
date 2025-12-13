<template>
  <div class="ocean-background-container">
    <div class="wave wave1"></div>
    <div class="wave wave2"></div>
  </div>
</template>

<script setup>
// このコンポーネントは純粋にCSSアニメーションで動作するため、JavaScriptは不要です
</script>

<style scoped>
/* =======================================
   1. コンテナ設定 (HomeView の背景を覆う)
   ======================================= */
.ocean-background-container {
  /* HomeView の home-container と同じサイズになるように絶対配置 */
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%; 
  overflow: hidden;
  /* 地図やヘッダーの下に配置 */
  z-index: 1; 
  
  /* ベースとなる海のグラデーション (HomeViewからこちらへ移動) */
  background: linear-gradient(to top, #b9daf6, #00255d); 
}

/* =======================================
   2. 波の基本スタイル
   ======================================= */
.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%; /* 画面幅の2倍にすることで、途切れないループを可能にする */
  height: 100%;
  
  /* 波の形状を生成するSVG背景 (今回は白っぽい波) */
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><path id="wavePath" d="M0 50 C25 80, 75 20, 100 50 L100 100 L0 100 Z" fill="white"/></defs><use href="#wavePath" transform="scale(2, 1.2)"/></svg>');
  background-size: 50% 120px; 
  background-repeat: repeat-x;
  background-position: bottom;
}

/* =======================================
   3. 各波レイヤーとアニメーション
   ======================================= */
.wave1 {
  opacity: 0.2;
  background-size: 150% 150px;
  animation: wave-move 20s linear infinite;
}

.wave2 {
  opacity: 0.1;
  background-size: 100% 100px;
  animation: wave-move 30s linear infinite;
  animation-delay: -10s; /* 開始タイミングをずらしてランダム感を出す */
}

@keyframes wave-move {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); } /* 幅の半分移動してループ */
}
</style>