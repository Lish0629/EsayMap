import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { mdi } from 'vuetify/iconsets/mdi';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const app = createApp(App)

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    sets: {
      mdi,
    },
  },
})

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.mount('#app')
