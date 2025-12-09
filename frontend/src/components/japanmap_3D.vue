<script setup>
const emit = defineEmits(['select'])

// 指定された7都市のピン定義
// top, left は「画像の上/左から何%の位置か」を指定
const pins = [
  { id: 1, name: '北海道', top: 15, left: 77 },
  { id: 2, name: '青森',   top: 28, left: 77 },
  { id: 15, name: '新潟',  top: 48, left: 67 },
  { id: 13, name: '東京',  top: 61.5, left: 72 },
  { id: 20, name: '長野',  top: 56, left: 61.5 },
  { id: 23, name: '愛知',  top: 66.6, left: 53.7 },
  { id: 27, name: '大阪',  top: 70, left: 43.2 },
]

const handleClick = (pin) => {
  emit('select', pin)
}
</script>

<template>
  <div class="map-container">
    <img src="/japan_map.png" alt="日本地図" class="map-image" />

    <div 
      v-for="pin in pins" 
      :key="pin.id"
      class="pin-wrapper"
      :style="{ top: pin.top + '%', left: pin.left + '%' }"
      @click="handleClick(pin)"
    >
      <div class="pin-icon">📍</div>
      <div class="pin-label">{{ pin.name }}</div>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.map-image {
  width: 100%;
  height: auto;
  display: block;
  /* 影をつけて浮遊感を出す */
  filter: drop-shadow(10px 15px 20px rgba(0,0,0,0.2));
}

.pin-wrapper {
  position: absolute;
  cursor: pointer;
  /* ピンの先端を中心にする */
  transform: translate(-50%, -90%);
  z-index: 10;
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pin-wrapper:hover {
  transform: translate(-50%, -120%) scale(1.3);
  z-index: 20;
}

.pin-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3));
}

.pin-label {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}

.pin-wrapper:hover .pin-label {
  opacity: 1;
}
</style>