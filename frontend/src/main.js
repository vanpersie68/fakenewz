import Vue from 'vue'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import axios from 'axios'
import vueRouter from 'vue-router'
import router from './router'
import i18n from './i18n'
import VueSweetalert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { devServer, publicPath } from '../vue.config'
import VueApexCharts from 'vue-apexcharts'
import 'element-ui/lib/theme-chalk/index.css'
import VueClipboard from 'vue-clipboard2'

import lottie from 'vue-lottie'

import './assets/icons/index.js'
Vue.component('lottie', lottie)

import VueCountdown from '@chenfengyuan/vue-countdown'
import $ from 'jquery'

// Vue.use(DatePicker);
Vue.component(VueCountdown.name, VueCountdown)
Vue.use($)

Vue.use(VueClipboard)
Vue.use(ElementUI, { locale })
Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.use(vueRouter)
Vue.use(VueSweetalert2)
library.add(fas)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(ElementUI)
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)
// axios.defaults.baseURL = 'http://35.220.143.92:8888/';
// axios.defaults.baseURL = 'https://cp13demoapi.piran.xyz/';
axios.defaults.baseURL = process.env.VUE_APP_SERVER
const lang = localStorage.getItem('lang') || 'en'
axios.defaults.headers['Accept-Language'] = lang

new Vue({
  i18n,
  render: (h) => h(App),
  router: router,
  beforeCreate() {
    Vue.prototype.$bus = this
  },
}).$mount('#app')
