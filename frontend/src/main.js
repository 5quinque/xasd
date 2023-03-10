import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import FloatingVue from 'floating-vue'

import './assets/main.scss'
import 'floating-vue/dist/style.css'

import 'bootstrap'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router)
app.use(FloatingVue)

app.mount('#app')
