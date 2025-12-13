import { createRouter, createWebHistory } from 'vue-router'

// 1. ページコンポーネントのインポート
// フォルダの場所が 'views' ではなく 'components' の場合は適宜パスを修正してください
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // ★ アプリを開いたとき、最初に表示するのはログイン画面
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      // ★ シミュレーションボタンを押したときの移動先（地図画面）
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      // ★ バトルボタンを押したときの移動先
      // （ファイルがまだないので、仮で HomeView を表示するか、後で BattleView.vue を作って差し替えてください）
      path: '/battle',
      name: 'battle',
      component: HomeView 
    },
    {
      // ★ 地図画面で検索したときの移動先（結果画面）
      path: '/result',
      name: 'result',
      // 結果画面のファイル名が ResultView.vue だと仮定しています。
      // まだファイルがない場合はエラーになるので、一旦 HomeView にしておくか、ファイルを作成してください。
      component: () => import('../views/ResultView.vue')
    }
  ]
})

export default router