import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

function loadLocaleMessages() {
  const locales = require('../src/locales')
  const messages = {}
  Object.keys(locales).forEach((key) => {
    messages[key] = locales[key]
  })

  return messages
}

export default new VueI18n({
  legacy: true,
  locale: localStorage.getItem('lang') || 'en',
  fallbackLocale: 'en',
  messages: loadLocaleMessages(),
})
