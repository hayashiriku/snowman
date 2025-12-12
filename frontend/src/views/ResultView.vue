<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SnowmanSvg from '../components/SnowmanSvg.vue'
import CityBackground from '../components/citybackground.vue'
import ComparisonObject from '../components/compar.vue'

const route = useRoute()
const router = useRouter()

const result = ref(null)
const isLoading = ref(true)
const errorMsg = ref('')

// --- レイアウト定数 ---
const STAGE_HEIGHT_PX = 450
const VISUAL_RATIO = 0.70      
const BOTTOM_OFFSET_RATIO = 0.09 
const ARROW_BOTTOM_OFFSET = 0   

// --- 比較対象データ ---
const COMPARISON_MASTER = [
  { name: "東京タワー", heightM: 333.0, imgUrl: "/images/tokyo_tower.png" },
  { name: "スカイツリー", heightM: 634.0, imgUrl: "/images/skytree.png" },
  { name: "富士山", heightM: 3776.0, imgUrl: "/images/fuji.png" },
  { name: "エベレスト", heightM: 8848.0, imgUrl: "/images/everest.png"}
]

onMounted(async () => {
  const { pref, date, type } = route.query
  if (!pref || !date || !type) {
    errorMsg.value = "データ不足です"
    isLoading.value = false
    return
  }
  try {
    const response = await fetch('http://localhost:8000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prefecture_id: parseInt(pref), target_date: date, period_type: type })
    })
    const data = await response.json()
    if (data.error) errorMsg.value = data.error
    else result.value = data
  } catch (e) {
    errorMsg.value = "通信エラー"
  } finally {
    isLoading.value = false
  }
})

// --- カメラ倍率計算 (添付ファイルのまま) ---
const pixelPerMeter = computed(() => {
  if (!result.value) return 10
  const h = result.value.height_m
  const visualHeightM = h / VISUAL_RATIO
  const viewHeightMeters = Math.max(visualHeightM * 1.2, 3.0)
  return STAGE_HEIGHT_PX / viewHeightMeters
})

// 比較対象の自動選択 (添付ファイルのまま)
const closestComparison = computed(() => {
  if (!result.value) return COMPARISON_MASTER[0]
  const h = result.value.height_m
  return COMPARISON_MASTER.reduce((prev, curr) => {
    return (Math.abs(curr.heightM - h) < Math.abs(prev.heightM - h)) ? curr : prev
  })
})

const goBack = () => router.push('/')
</script>

<template>
  <div class="result-page">
    <div v-if="isLoading" class="loading-view"><div class="spinner">❄️</div><h2>作成中...</h2></div>
    <div v-else-if="errorMsg" class="error-view"><h2>エラー</h2><p>{{ errorMsg }}</p><button class="back-btn" @click="goBack">戻る</button></div>

    <div v-else-if="result" class="content-view">
      <div class="header-area">
        <h1>🎉 完成！</h1>
        <p class="pref-msg">{{ result.message }}</p>
      </div>

      <div class="visual-stage">
        <CityBackground :scale="pixelPerMeter / VISUAL_RATIO" />

        <div class="scroll-container">
          
          <div class="main-figures-wrapper">
            
            <div class="comparison-container">
              
              <ComparisonObject 
                :height-px="closestComparison.heightM * pixelPerMeter"
                :img-url="closestComparison.imgUrl"
                :name="closestComparison.name"
                class="comp-obj"
                :style="{ 
                  transform: `translateY(${ (closestComparison.heightM * pixelPerMeter) * (closestComparison.offsetRatio || 0) }px)`
                }"
              />

              <div 
                class="dimension-box right-pos" 
                :style="{ height: (closestComparison.heightM * pixelPerMeter) + 'px' }"
              >
                <div class="dim-line" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-bar-top"></div>
                <div class="dim-arrow-top"></div>
                <div class="dim-arrow-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-bar-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-label">{{ closestComparison.heightM.toLocaleString() }}m</div>
              </div>

            </div>

            <div class="snowman-container">

              <div 
                class="dimension-box" 
                :style="{ 
                  height: (result.height_m * pixelPerMeter) + 'px',
                }"
              >
                <div class="dim-line" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-bar-top"></div>
                <div class="dim-arrow-top"></div>
                <div class="dim-arrow-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-bar-bottom" :style="{ bottom: ARROW_BOTTOM_OFFSET + 'px' }"></div>
                <div class="dim-label">{{ result.height_m.toFixed(1) }}m</div>
              </div>

              <SnowmanSvg 
                :height-px="((result.height_m * pixelPerMeter) +25)/ VISUAL_RATIO" 
                :style="{ 
                  transform: `translateY(${ ((result.height_m * pixelPerMeter) / VISUAL_RATIO) * BOTTOM_OFFSET_RATIO }px)` 
                }"
              />
              
            </div>

          </div>
        </div>
      </div>

      <div class="stats-box">
        <div class="stat-item"><span class="sub">高さ</span><span class="val highlight">{{ result.height_m.toFixed(1) }}</span><span class="unit">m</span></div>
        <div class="stat-item"><span class="sub">総体積</span><span class="val">{{ result.volume_m3.toLocaleString() }}</span><span class="unit">m³</span></div>
      </div>

      <button class="back-btn" @click="goBack">もう一度作る</button>
    </div>
  </div>
</template>

<style scoped>
.result-page { min-height: 100vh; background: linear-gradient(to bottom, #e1f5fe, #fff); display: flex; flex-direction: column; align-items: center; padding: 20px; font-family: sans-serif; color: #333; }
.content-view { width: 100%; max-width: 900px; animation: slideIn 0.5s ease-out; }
@keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.loading-view { margin-top: 100px; text-align: center; color: #0288d1; }
.spinner { font-size: 4rem; display: inline-block; animation: spin 1.5s infinite linear; margin-bottom: 20px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
.header-area { text-align: center; margin-bottom: 20px; }
h1 { color: #e65100; margin: 0; font-size: 2rem; }
.pref-msg { background: white; display: inline-block; padding: 8px 20px; border-radius: 20px; margin-top: 10px; font-weight: bold; color: #0277bd; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

/* --- ステージ全体のレイアウト --- */
.visual-stage {
  position: relative; 
  width: 100%; 
  height: 450px; 
  overflow: hidden; 
  border-bottom: 10px solid #3e2723; 
  margin-bottom: 30px; 
  border-radius: 12px; 
  background-color: #E0F7FA; 
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.scroll-container {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  overflow-x: auto; 
  overflow-y: hidden;
  display: flex;
  align-items: flex-end; 
}

.main-figures-wrapper {
  position: relative;
  z-index: 10;
  margin: 0 auto; 
  min-width: 100%; 
  width: fit-content; 
  height: 100%;
  
  display: flex;
  align-items: flex-end;
  justify-content: center;
  
  padding: 0 50px; 
  box-sizing: border-box; 
  gap: 80px; 
}

/* 比較対象コンテナ */
.comparison-container {
  position: relative;
  display: flex;
  align-items: flex-end; 
  flex-shrink: 0; 
  margin-right: 30px; 
}

/* 雪だるまコンテナ */
.snowman-container {
  position: relative;
  display: flex;
  align-items: flex-end;
  flex-shrink: 0; 
}

/* 画像や雪だるま本体 */
.comp-obj {
  /* スタイルはインラインで制御 */
}

/* --- 寸法線 (共通設定: 左配置用) --- */
.dimension-box {
  position: relative;
  width: 0px; 
  margin-right: -45px; /* 左配置時に画像に寄せる設定 */
  z-index: 20; 
  transition: all 0.5s ease-out;
}

/* ★追加: 右配置用のスタイル上書き */
.dimension-box.right-pos {
  margin-right: 0;   /* 左用のマイナスマージンをリセット */
  margin-left: 5px;  /* 画像の右側に少し隙間を空けて配置 */
}

.dim-line { position: absolute; top: 0; bottom: 0; left: 10px; width: 2px; background-color: #ffffff; box-shadow: 1px 0 2px rgba(0,0,0,0.3); }
.dim-bar-top, .dim-bar-bottom { position: absolute; left: 11px; transform: translateX(-50%); width: 20px; height: 2px; background-color: #ffffff; z-index: 5; box-shadow: 0 1px 2px rgba(0,0,0,0.3); }
.dim-bar-top { top: 0; }
.dim-arrow-top { position: absolute; top: 0; left: 11px; transform: translateX(-50%); width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 10px solid #ffffff; }
.dim-arrow-bottom { position: absolute; bottom: 0; left: 11px; transform: translateX(-50%); width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 10px solid #ffffff; }
.dim-label { position: absolute; top: 50%; left: 10px; transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7); color: #ffffff; border: 1px solid #ffffff; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 1rem; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.2); z-index: 10; }

/* --- 統計表示 --- */
.stats-box { display: flex; justify-content: center; gap: 40px; margin-bottom: 30px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.stat-item { display: flex; flex-direction: column; align-items: center; }
.sub { font-size: 0.8rem; color: #888; }
.val { font-size: 1.8rem; font-weight: bold; color: #333; }
.val.highlight { color: #e65100; }
.unit { font-size: 1rem; margin-left: 2px; }
.back-btn { display: block; margin: 0 auto; background: #0288d1; color: white; border: none; padding: 15px 50px; font-size: 1.2rem; font-weight: bold; border-radius: 50px; cursor: pointer; box-shadow: 0 5px 15px rgba(2, 137, 209, 0.4); transition: transform 0.2s; }
.back-btn:hover { transform: scale(1.05); background: #0277bd; }
</style>