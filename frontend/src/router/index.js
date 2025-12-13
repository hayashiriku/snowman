import { createRouter, createWebHistory } from 'vue-router'

// 1. 各画面のコンポーネントをインポート
import LoginView from '../views/LoginView.vue'   // スタート画面
import HomeView from '../views/HomeView.vue'     // シミュレーション（地図）画面
import ResultView from '../views/ResultView.vue' // ★結果画面（今回追加）
import BattleView from '../views/BattleView.vue' // バトル設定画面

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // アプリ起動時はログイン（スタート）画面
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      // シミュレーションモードの地図画面
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      // ★シミュレーション結果画面
      // HomeView.vue から router.push('/result') されたらここに来ます
      path: '/result',
      name: 'result',
      component: ResultView
    },
    {
      // バトルモード設定画面
      path: '/battle',
      name: 'battle',
      component: BattleView
    },
    {
      // バトル結果画面（仮）
      // まだファイルがない場合は HomeView などを仮置きしておきます
      path: '/battle-result',
      name: 'battle-result',
      component: HomeView 
    }
  ]
})

export default router