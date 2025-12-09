<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: Date // 親から受け取る日付
})

const emit = defineEmits(['update:modelValue', 'search'])

// 内部で管理する表示用年月
const displayDate = ref(new Date(props.modelValue || new Date()))

// 年・月・日を取得
const year = computed(() => displayDate.value.getFullYear())
const month = computed(() => displayDate.value.getMonth() + 1)

// カレンダー生成ロジック
const calendarDays = computed(() => {
  const year = displayDate.value.getFullYear()
  const month = displayDate.value.getMonth()
  const lastDay = new Date(year, month + 1, 0).getDate()
  const firstDayOfWeek = new Date(year, month, 1).getDay()
  
  const days = []
  // 空白埋め
  for (let i = 0; i < firstDayOfWeek; i++) days.push(null)
  // 日付埋め
  for (let i = 1; i <= lastDay; i++) days.push(i)
  return days
})

// --- アクション ---

// 月移動
const addMonth = (n) => {
  const d = new Date(displayDate.value)
  d.setMonth(d.getMonth() + n)
  displayDate.value = d
}

// 共通: 親に変更を伝える関数
const trigger = (type, day = null) => {
  const d = new Date(displayDate.value)
  if (day) d.setDate(day)
  
  // 親のv-modelを更新
  emit('update:modelValue', d)
  
  // 「どのモードで検索するか」を通知
  // type: 'year' | 'month' | 'day'
  emit('search', type)
}

// 判定用: 選択中の日付か？
const isSelected = (day) => {
  if (!day || !props.modelValue) return false
  const p = props.modelValue
  const d = displayDate.value
  return p.getDate() === day && p.getMonth() === d.getMonth() && p.getFullYear() === d.getFullYear()
}
</script>

<template>
  <div class="calendar-card">
    <div class="header">
      <button class="nav-btn" @click="addMonth(-1)">&lt;</button>
      
      <div class="date-labels">
        <span class="label year-label" @click="trigger('year')">
          {{ year }}年
          <span class="tooltip">年間降雪量</span>
        </span>
        
        <span class="label month-label" @click="trigger('month')">
          {{ month }}月
          <span class="tooltip">月間降雪量</span>
        </span>
      </div>

      <button class="nav-btn" @click="addMonth(1)">&gt;</button>
    </div>

    <div class="grid weeks">
      <span class="sun">日</span><span>月</span><span>火</span><span>水</span><span>木</span><span>金</span><span class="sat">土</span>
    </div>

    <div class="grid days">
      <div 
        v-for="(day, idx) in calendarDays" 
        :key="idx"
        class="day-cell"
        :class="{ 'empty': !day, 'selected': isSelected(day) }"
        @click="day && trigger('day', day)"
      >
        {{ day }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border: 1px solid #eee;
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
  user-select: none;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.date-labels {
  display: flex;
  gap: 10px;
  font-size: 1.2rem;
  font-weight: bold;
}

/* 年と月のラベル (クリック可能に見せる) */
.label {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
  position: relative; /* ツールチップ用 */
}
.year-label:hover { background: #e3f2fd; color: #0288d1; }
.month-label:hover { background: #e8f5e9; color: #2e7d32; }

/* ホバー時に出るツールチップ */
.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
  white-space: nowrap;
}
.label:hover .tooltip { opacity: 1; }

.nav-btn {
  background: #f5f5f5; border: none;
  width: 30px; height: 30px; border-radius: 50%;
  cursor: pointer; font-weight: bold; color: #666;
}
.nav-btn:hover { background: #e0e0e0; }

.grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  gap: 5px;
}
.weeks { margin-bottom: 10px; font-size: 0.85rem; color: #888; font-weight: bold; }
.sun { color: #e57373; }
.sat { color: #64b5f6; }

.day-cell {
  height: 36px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.95rem;
  transition: 0.2s;
}
.day-cell:not(.empty):hover { background: #e0f7fa; color: #006064; }
.day-cell.selected { background: #0288d1; color: white; font-weight: bold; }
.empty { cursor: default; }
</style>