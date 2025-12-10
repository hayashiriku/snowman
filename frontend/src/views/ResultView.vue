<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SnowmanSvg from '../components/SnowmanSvg.vue'
import CityBackground from '../components/citybackground.vue'

const route = useRoute()
const router = useRouter()

const result = ref(null)
const isLoading = ref(true)
const errorMsg = ref('')

// --- ★調整用の設定パラメータ ---

const STAGE_HEIGHT_PX = 450

// 1. 画像の「絵」の割合
// 画像の上部に透明な余白があるため、「画像の高さの85%が実際の絵」として扱います。
// これで寸法線と頭のてっぺんが合います。
const VISUAL_RATIO = 0.83 

// 2. 雪だるまを沈める割合
// 画像の下部にも透明な余白があるため、画像の高さの8%分だけ下にずらして接地させます。
const BOTTOM_OFFSET_RATIO = 0.08

// 3. 矢印の底上げ調整 (px)
// 雪だるまの底面のカーブに合わせて、寸法線の下矢印を少し上にずらします。
const ARROW_BOTTOM_OFFSET = 4 

const LINE_HEIGHT_RATIO = 0.81

// --------------------------------

onMounted(async () => {
  const { pref, date, type } = route.query
  if (!pref || !date || !type) {
    errorMsg.value = "データ不足です。トップに戻ってください。"
    isLoading.value = false
    return
  }

  try {
    const response = await fetch('http://localhost:8000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prefecture_id: parseInt(pref),
        target_date: date,
        period_type: type
      })
    })
    const data = await response.json()
    
    if (data.error) errorMsg.value = data.error
    else result.value = data
  } catch (e) {
    errorMsg.value = "サーバー通信エラーが発生しました。"
  } finally {
    isLoading.value = false
  }
})

// --- カメラのズーム倍率計算 ---
// 雪だるまのサイズに合わせて、街並みや雪だるまの描画サイズ(scale)を決定します
const pixelPerMeter = computed(() => {
  if (!result.value) return 10
  
  const h = result.value.height_m
  
  // 余計な「最低500m」などの制限を撤廃しました。
  // 雪だるまの高さの1.3倍の範囲を画面に収めます。
  // (ただし、1m以下の小さすぎる時だけバグ防止で最低3mは確保します)
  const viewHeightMeters = Math.max(h * 1.3, 3.0) 
  
  return STAGE_HEIGHT_PX / viewHeightMeters
})

const goBack = () => router.push('/')
</script>

<template>
  <div class="result-page">
    
    <div v-if="isLoading" class="loading-view">
      <div class="spinner">❄️</div>
      <h2>雪を集めています...</h2>
    </div>

    <div v-else-if="errorMsg" class="error-view">
      <h2>⚠️ エラー</h2>
      <p>{{ errorMsg }}</p>
      <button class="back-btn" @click="goBack">戻る</button>
    </div>

    <div v-else-if="result" class="content-view">
      <div class="header-area">
        <h1>🎉 完成！</h1>
        <p class="pref-msg">{{ result.message }}</p>
      </div>

      <div class="visual-stage">
        
        <CityBackground :scale="pixelPerMeter" />

        <div class="figure-wrapper standard street-position">
          <SnowmanSvg 
            :height-px="(1.0 * pixelPerMeter) / VISUAL_RATIO"
            :style="{ 
              transform: `translateY(${ ((1.0 * pixelPerMeter) / VISUAL_RATIO) * BOTTOM_OFFSET_RATIO }px)` 
            }" 
          />
          <div class="label">基準(1m)</div>
        </div>

        <div class="figure-wrapper result giant-position">
          
          <SnowmanSvg 
            :height-px="(result.height_m * pixelPerMeter) / VISUAL_RATIO" 
            :style="{ 
              transform: `translateY(${ ((result.height_m * pixelPerMeter) / VISUAL_RATIO) * BOTTOM_OFFSET_RATIO }px)` 
            }"
          />
          
          <div class="dimension-box" :style="{ height: (result.height_m * pixelPerMeter * LINE_HEIGHT_RATIO) + 'px' }">
            
            <div class="dim-line" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>

            <div class="dim-bar-top"></div>
            
            <div class="dim-arrow-top"></div>
            
            <div class="dim-arrow-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>

            <div class="dim-bar-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
            
            <div class="dim-label">
              {{ result.height_m.toFixed(1) }}m
            </div>
          </div>

        </div>

      </div>

      <div class="stats-box">
        <div class="stat-item">
          <span class="sub">高さ</span>
          <span class="val highlight">{{ result.height_m.toFixed(1) }}</span>
          <span class="unit">m</span>
        </div>
        <div class="stat-item">
          <span class="sub">総体積</span>
          <span class="val">{{ result.volume_m3.toLocaleString() }}</span>
          <span class="unit">m³</span>
        </div>
      </div>

      <button class="back-btn" @click="goBack">もう一度作る</button>
    </div>
  </div>
</template>

<style scoped>
/* --- 全体のレイアウト --- */
.result-page { 
  min-height: 100vh; 
  background: linear-gradient(to bottom, #e1f5fe, #fff); 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  padding: 20px; 
  font-family: sans-serif; 
  color: #333; 
}

.content-view { width: 100%; max-width: 900px; animation: slideIn 0.5s ease-out; }
@keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

/* ロード中・エラー */
.loading-view { margin-top: 100px; text-align: center; color: #0288d1; }
.spinner { font-size: 4rem; display: inline-block; animation: spin 1.5s infinite linear; margin-bottom: 20px; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.header-area { text-align: center; margin-bottom: 20px; }
h1 { color: #e65100; margin: 0; font-size: 2rem; }
.pref-msg { background: white; display: inline-block; padding: 8px 20px; border-radius: 20px; margin-top: 10px; font-weight: bold; color: #0277bd; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

/* --- ビジュアルステージ --- */
.visual-stage {
  position: relative;
  width: 100%;
  height: 450px;
  overflow: hidden; /* ビルのはみ出し防止 */
  border-bottom: 10px solid #3e2723; /* 地面 */
  margin-bottom: 30px;
  border-radius: 12px;
  background-color: #E0F7FA; /* 空の色 */
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

/* 雪だるまラッパー */
.figure-wrapper {
  position: absolute;
  bottom: 0px; /* 少し埋まるくらいの位置を基準にする */
  display: flex;
  flex-direction: row;   /* 横並び */
  align-items: flex-end; /* 下揃え */
  gap: 15px;             /* 雪だるまと寸法線の間隔 */
  transition: all 0.5s ease-out;
}

.street-position { left: 15%; z-index: 20; }
.giant-position { left: 60%; transform: translateX(-50%); z-index: 15; }

/* ラベル (基準雪だるま用) */
.label { 
  margin-left: 10px; /* 横並びになったので少し調整 */
  margin-bottom: 20px;
  font-weight: bold; font-size: 0.8rem; 
  background: rgba(255,255,255,0.9); padding: 4px 8px; border-radius: 4px; 
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); white-space: nowrap; 
}

/* --- 寸法線のデザイン (白線) --- */

.dimension-box {
  position: relative;
  width: 50px;
  /* heightはインラインスタイルで動的に指定 */
}

/* 縦線 */
.dim-line {
  position: absolute;
  top: 0; bottom: 0; left: 15px;
  width: 2px;
  background-color: #ffffff; /* 白 */
}

/* --- ★新規追加: 矢印の先の横線 (Tバー) --- */

.dim-bar-top, .dim-bar-bottom {
  position: absolute;
  left: 16px; /* 矢印の中心(16px)に合わせる */
  transform: translateX(-50%); /* 真ん中合わせ */
  width: 20px; /* 横線の長さ */
  height: 2px; /* 線の太さ */
  background-color: #ffffff; /* 線の色 (白) */
  z-index: 5;
}

/* 上の横線は一番上 */
.dim-bar-top {
  top: 0;
}

/* 下の横線は bottom 指定を HTML 側の style で行うので、ここは空でOK */
.dim-bar-bottom {
  /* positionなどは共通設定で適用済み */
}

/* 上の矢印 */
.dim-arrow-top {
  position: absolute;
  top: 0; left: 16px;
  transform: translateX(-50%);
  width: 0; height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 10px solid #ffffff; /* 白 */
}

/* 下の矢印 */
.dim-arrow-bottom {
  position: absolute;
  bottom: 0; left: 16px;
  transform: translateX(-50%);
  width: 0; height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 10px solid #ffffff; /* 白 */
}

/* 数値ラベル */
.dim-label {
  position: absolute;
  top: 50%; left: 15px;
  transform: translate(-50%, -50%); /* 中央配置 */
  
  background-color: rgba(0, 0, 0, 0.6); /* 半透明黒背景 */
  color: #ffffff; /* 白文字 */
  border: 1px solid #ffffff; /* 白枠 */
  
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 1rem;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 10;
}

/* --- 統計ボックス --- */
.stats-box { 
  display: flex; justify-content: center; gap: 40px; margin-bottom: 30px; 
  background: white; padding: 20px; border-radius: 12px; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
}
.stat-item { display: flex; flex-direction: column; align-items: center; }
.sub { font-size: 0.8rem; color: #888; }
.val { font-size: 1.8rem; font-weight: bold; color: #333; }
.val.highlight { color: #e65100; }
.unit { font-size: 1rem; margin-left: 2px; }

/* ボタン */
.back-btn { 
  display: block; margin: 0 auto; 
  background: #0288d1; color: white; border: none; padding: 15px 50px; 
  font-size: 1.2rem; font-weight: bold; border-radius: 50px; cursor: pointer; 
  box-shadow: 0 5px 15px rgba(2, 137, 209, 0.4); transition: transform 0.2s; 
}
.back-btn:hover { transform: scale(1.05); background: #0277bd; }
</style>