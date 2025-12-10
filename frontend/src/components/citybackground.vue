<script setup>
defineProps({
  scale: { type: Number, default: 1 }
})

// 現実的なサイズ感の建物データ (メートル)
const buildings = [
  // 奥のレイヤー：巨大な摩天楼など
  { id: 1, heightM: 150, widthM: 40, color: '#90a4ae', layer: 'far', left: '5%' },
  { id: 2, heightM: 80,  widthM: 30, color: '#78909c', layer: 'far', left: '70%' },
  
  // 手前のレイヤー：マンション、オフィス、家
  { id: 3, heightM: 40,  widthM: 25, color: '#cfd8dc', layer: 'near', left: '15%' }, // 10階建てビル
  { id: 4, heightM: 60,  widthM: 35, color: '#b0bec5', layer: 'near', left: '45%' }, // 15階建てビル
  { id: 5, heightM: 8,   widthM: 12, color: '#d7ccc8', layer: 'near', left: '85%' }, // 2階建ての家 (小さい！)
]
</script>

<template>
  <div class="city-container">
    <div class="sky"></div>
    
    <div 
      v-for="b in buildings" 
      :key="b.id"
      class="building"
      :class="b.layer"
      :style="{
        height: (b.heightM * scale) + 'px', 
        width:  (b.widthM  * scale) + 'px',
        left: b.left,
        backgroundColor: b.color
      }"
    >
      <div v-if="b.layer === 'near'" class="windows"></div>
    </div>

    <div class="ground"></div>
  </div>
</template>

<style scoped>
.city-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: 0; }
.sky { position: absolute; top: 0; left: 0; width: 100%; height: 80%; background: linear-gradient(to bottom, #87CEEB, #E0F7FA); }
.ground { position: absolute; bottom: 0; left: 0; width: 100%; height: 20px; background: #3e2723; z-index: 10; }

.building { position: absolute; bottom: 20px; border: 2px solid #546e7a; border-bottom: none; transition: all 0.5s ease-out; }
.far { opacity: 0.6; z-index: 1; }
.near { z-index: 2; box-shadow: 5px 0 10px rgba(0,0,0,0.1); }

.windows {
  position: absolute; top: 5%; left: 10%; right: 10%; bottom: 0;
  background-image: linear-gradient(rgba(255,255,255,0.8) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.8) 2px, transparent 2px);
  background-size: 20% 3%; background-color: #455a64;
}
</style>