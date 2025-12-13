<template>
  <div class="snow-area" ref="canvasContainer">
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

const canvasContainer = ref(null); // DOM要素への参照
let animationFrameId; // requestAnimationFrame のID
let resizeListener; // リサイズイベントリスナー

const runSnowAnimation = (masthead) => {
    
    // ===============================================
    // ★ ユーザーから提供されたCanvasコードの移植
    // ===============================================

    var COUNT = 200;
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var width = masthead.clientWidth;
    var height = masthead.clientHeight;
    var i = 0;
    var active = false;

    function onResize() {
      width = masthead.clientWidth;
      height = masthead.clientHeight;
      canvas.width = width;
      canvas.height = height;
      ctx.fillStyle = '#FFF';

      var wasActive = active;
      active = width > 200;

      if (!wasActive && active)
        requestAnimFrame(update);
    }

    var Snowflake = function () {
      this.x = 0;
      this.y = 0;
      this.vy = 0;
      this.vx = 0;
      this.r = 0;

      this.reset();
    }

    Snowflake.prototype.reset = function() {
      this.x = Math.random() * width;
      this.y = Math.random() * -height;
      this.vy = 0.5 + Math.random() * 2;
      this.vx = 0.3 - Math.random();
      this.r = 0.5 + Math.random() * 1.5;
      this.o = 0.3 + Math.random() * 0.5;
    }

    var snowflakes = [], snowflake;
    for (i = 0; i < COUNT; i++) {
      snowflake = new Snowflake();
      snowflake.reset();
      snowflakes.push(snowflake);
    }

    function update() {

      ctx.clearRect(0, 0, width, height);

      if (!active)
        return;

      for (i = 0; i < COUNT; i++) {
        snowflake = snowflakes[i];
        snowflake.y += snowflake.vy;
        snowflake.x += snowflake.vx;

        ctx.globalAlpha = snowflake.o;
        ctx.beginPath();
        // Math.PI * 5 を Math.PI * 2 (360度) に修正
        ctx.arc(snowflake.x, snowflake.y, snowflake.r, 0, Math.PI * 2, false);
        ctx.closePath();
        ctx.fill();

        if (snowflake.y > height) {
          snowflake.reset();
        }
      }

      animationFrameId = requestAnimFrame(update);
    }

    window.requestAnimFrame = (function(){
      return  window.requestAnimationFrame       ||
                window.webkitRequestAnimationFrame ||
                window.mozRequestAnimationFrame    ||
                function( callback ){
                  window.setTimeout(callback, 1000 / 60);
                };
    })();

    onResize();
    masthead.appendChild(canvas);
    
    // リサイズリスナーを定義し、unmounted で削除できるように保存
    resizeListener = onResize;
    window.addEventListener('resize', resizeListener, false);
    
    // ===============================================
};


onMounted(() => {
    if (canvasContainer.value) {
        runSnowAnimation(canvasContainer.value);
    }
});

onUnmounted(() => {
    // クリーンアップ
    if (animationFrameId) {
        // requestAnimationFrame の終了
        cancelAnimationFrame(animationFrameId); 
    }
    // リサイズイベントリスナーの削除
    if (resizeListener) {
        window.removeEventListener('resize', resizeListener, false);
    }
});
</script>

<style scoped>
/* =======================================
   1. 雪のコンテナ (最前面に固定)
   ======================================= */
.snow-area {
  position: absolute; 
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  pointer-events: none; /* クリックイベントを通過させる */
  overflow: hidden; 
  z-index: 100; /* 地図やモーダルより確実に手前に */
}

/* =======================================
   2. Canvas要素のスタイル (JSが生成する要素)
   ======================================= */
/* Vue 3 では :deep() 擬似要素を使って子コンポーネントのスタイルを適用 */
.snow-area :deep(canvas) {
    position: absolute;
    top: 0;
    left: 0;
}
</style>