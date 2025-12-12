<script setup>
defineProps({
  heightPx: Number,
  name: String,
  imgUrl: String
})
</script>

<template>
  <div class="comp-wrapper" :style="{ height: heightPx + 'px' }">
    <div class="image-container">
      <img :src="imgUrl" :alt="name" class="comp-image" />
    </div>
    <div class="comp-info">
      <div class="comp-name">{{ name }}</div>
    </div>
  </div>
</template>

<style scoped>
.comp-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end; /* 地面に合わせる */
  position: relative;
  width: auto;
  transition: height 0.5s ease-out;
}

.image-container {
  height: 100%;
  display: flex;
  align-items: flex-end; /* 画像の下端を合わせる */
  justify-content: center;
}

.comp-image {
  height: 100% !important; /* 計算された高さに画像を強制的に合わせる */
  width: auto;
  object-fit: contain;
  filter: drop-shadow(5px 5px 15px rgba(0,0,0,0.3));
}

.comp-info {
  position: absolute;
  bottom: -30px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  white-space: nowrap;
  pointer-events: none;
  z-index: 10;
}
</style>