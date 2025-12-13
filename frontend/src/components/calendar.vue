<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  modelValue: Date, // 親から受け取る日付
  prefId: Number    // 親から受け取る県ID
})

const emit = defineEmits(['update:modelValue', 'search'])

const displayDate = ref(new Date(props.modelValue || new Date()))

// データ状態を管理するオブジェクト
// 例: { "2024-02-01": "positive", "2024-02-02": "zero" }
const availableDates = ref({})

onMounted(async () => {
  try {
    // 親から県IDが渡されていない場合はAPIを叩かない（エラー防止）
    if (!props.prefId) return

    const res = await fetch(`http://localhost:8000/available_dates?pref_id=${props.prefId}`)
    if (res.ok) {
      availableDates.value = await res.json()
    }
  } catch (e) {
    console.error("日付データの取得に失敗しました", e)
  }
})

const year = computed(() => displayDate.value.getFullYear())
const month = computed(() => displayDate.value.getMonth() + 1)

const calendarDays = computed(() => {
  const year = displayDate.value.getFullYear()
  const month = displayDate.value.getMonth()
  const lastDay = new Date(year, month + 1, 0).getDate()
  const firstDayOfWeek = new Date(year, month, 1).getDay()
  
  const days = []
  for (let i = 0; i < firstDayOfWeek; i++) days.push(null)
  for (let i = 1; i <= lastDay; i++) days.push(i)
  return days
})

const getDataStatus = (day) => {
  if (!day) return null
  const y = displayDate.value.getFullYear()
  const m = String(displayDate.value.getMonth() + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  const dateStr = `${y}-${m}-${d}`
  
  return availableDates.value[dateStr]
}

const addMonth = (n) => {
  const d = new Date(displayDate.value)
  d.setMonth(d.getMonth() + n)
  displayDate.value = d
}

const trigger = (type, day = null) => {
  const d = new Date(displayDate.value)
  if (day) d.setDate(day)
  emit('update:modelValue', d)
  emit('search', type)
}

const isToday = (day) => {
  if (!day) return false
  const d = new Date()
  return d.getFullYear() === displayDate.value.getFullYear() &&
         d.getMonth() === displayDate.value.getMonth() &&
         d.getDate() === day
}

const isSelected = (day) => {
  if (!day || !props.modelValue) return false
  const d = new Date(props.modelValue)
  return d.getFullYear() === displayDate.value.getFullYear() &&
         d.getMonth() === displayDate.value.getMonth() &&
         d.getDate() === day
}
</script>

<template>
  <div class="calendar-container">
    <div class="header">
      <button class="nav-btn" @click="addMonth(-1)">‹</button>
      <div class="current-month">
        <span class="label year-label">{{ year }}年</span>
        <span class="label month-label">{{ month }}月</span>
      </div>
      <button class="nav-btn" @click="addMonth(1)">›</button>
    </div>

    <div class="weekdays">
      <span v-for="w in ['日','月','火','水','木','金','土']" :key="w" :class="{ 'sunday': w==='日', 'saturday': w==='土' }">{{ w }}</span>
    </div>

    <div class="calendar-grid">
      <div v-for="(day, index) in calendarDays" :key="index" 
           class="day-cell" 
           :class="{ 
             'empty': !day, 
             'today': isToday(day),
             'selected': isSelected(day),
             'clickable': day
           }"
           @click="day && trigger('day', day)">
        
        <span class="day-num">{{ day }}</span>
        
        <div 
          v-if="getDataStatus(day)" 
          class="data-dot" 
          :class="getDataStatus(day)"
        ></div>
        
      </div>
    </div>
    
    <div class="calendar-legend">
      <div class="legend-item">
        <span class="legend-dot positive"></span>
        <span>作れる日</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot zero"></span>
        <span>雪不足</span>
      </div>
    </div>

  </div>
</template>

<style scoped>
.calendar-container {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  font-family: sans-serif;
  user-select: none;
  padding-bottom: 15px; /* 下部余白を少し増やす */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 10px;
}
.current-month {
  display: flex;
  gap: 10px;
  font-size: 1.2rem; 
  font-weight: bold;
}
.label { cursor: pointer; padding: 4px 8px; border-radius: 6px; transition: background 0.2s; }
.label:hover { background: #f5f5f5; }
.nav-btn {
  background: #f5f5f5; border: none;
  width: 30px; height: 30px; border-radius: 50%;
  cursor: pointer; font-weight: bold; color: #666;
  transition: background 0.2s;
}
.nav-btn:hover { background: #e0e0e0; }

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-size: 0.8rem; 
  color: #888;
  margin-bottom: 5px;
  margin-top: 5px;
}
.sunday { color: #e57373; }
.saturday { color: #64b5f6; }

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  margin-bottom: 15px; /* 説明との間隔をあける */
}
.day-cell {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
  color: #333;
  transition: all 0.2s;
  position: relative;
}
.day-cell:hover:not(.empty) {
  background-color: #fce4ec;
  color: #e91e63;
}
.empty { cursor: default; }

.today { border: 2px solid #e65100; color: #e65100; }

.selected {
  background-color: #e65100 !important;
  color: white !important;
  box-shadow: 0 4px 10px rgba(230, 81, 0, 0.4);
}
.selected .data-dot { background-color: white !important; }

/* 点のスタイル */
.data-dot {
  width: 5px; 
  height: 5px;
  border-radius: 50%;
  margin-top: 2px; 
}
.data-dot.positive { background-color: #e65100; }
.data-dot.zero { background-color: #039be5; }

/* ★追加: 凡例のスタイル */
.calendar-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
  font-size: 0.85rem;
  color: #666;
  background-color: #f9f9f9; /* 少し背景色をつけてエリアを分ける */
  padding: 8px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.legend-dot.positive { background-color: #e65100; }
.legend-dot.zero { background-color: #039be5; }
</style>