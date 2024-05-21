<template>
  <div class="LangDropDown">
    <select v-model="$i18n.locale" @change="onChange($event)">
      <option value="en">English</option>
      <option value="kn">ಕನ್ನಡ</option>
      <option value="ja">日本語</option>
      <option value="ur">اردو</option>
      <option value="hi">हिंदी</option>
      <option value="zh">中文（简体)</option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'LanguageDropDown',
  methods: {
    /**
     * Handle language change
     * @param event - change event
     */
    onChange(event) {
      console.log(event.target.value)
      document.documentElement.lang = event.target.value
    },
  },
}
</script>

<style scoped>
select {
  padding: 10px;
  background: none;
  border: 1px solid #fff;
  border-radius: 3px;
  color: #fff;
}
option {
  color: black;
}

.LangList {
  color: #000;
}

.LangDropDown {
  margin-right: 20px;
}
</style>
