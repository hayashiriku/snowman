<script setup>
// 親から「高さ(px)」を受け取る
defineProps({
  heightPx: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <img 
    src="/snowman.svg" 
    alt="雪だるま"
    class="snowman-img"
    :style="{ height: heightPx + 'px' }"
  />
</template>

<style scoped>
.snowman-img {
  /* 高さが変わると滑らかにアニメーション */
  transition: height 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  
  /* 下揃えにするための設定 */
  display: block;
  margin: 0 auto;
  
  /* 画像の幅は高さに合わせて自動調整(アスペクト比維持) */
  width: auto;
  
  /* 少し影をつけるとおしゃれ */
  filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.2));
}
</style>