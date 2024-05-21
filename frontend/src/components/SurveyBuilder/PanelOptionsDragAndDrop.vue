<template>
  <div class="options">
    <h1 class="close-header">{{ $t('pOptionsDnD.numChips') }}</h1>
    <text-box-num
      :value="question.choices.length.toString()"
      @update="
        (value) =>
          $store.commit('updateMultiList', { question: question, value: value })
      "
      :key="question.choices.length"
      @increment="
        $store.commit('insertLastElement', {
          list: question.choices,
          element: { text: $t('app.item') },
        })
      "
      @decrement="$store.commit('removeLastElement', question.choices)"
    />

    <line-base class="dark" />

    <h1 class="close-header">{{ $t('pOptionsDnD.numCategories') }}</h1>
    <text-box-num
      :value="question.categories.length.toString()"
      @update="
        (value) =>
          $store.commit('updateMultiList', { question: question, value: value })
      "
      :key="question.categories.length"
      @increment="
        $store.commit('insertLastElement', {
          list: question.categories,
          element: { text: $t('app.category') },
        })
      "
      @decrement="$store.commit('removeLastElement', question.categories)"
    />

    <line-base class="dark" />
  </div>
</template>

<script>
import LineBase from './LineBase.vue'
import TextBoxNum from './TextBoxNum.vue'

export default {
  name: 'PanelOptionsMultipleChoice',
  components: {
    LineBase,
    TextBoxNum,
  },
  props: {
    question: Object,
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

.close-header {
  padding-bottom: 0px;
}

h1,
h2 {
  color: black;
  padding: 0 16px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  text-align: left;
}

h1 {
  font-size: 16px;
  font-weight: bold;
  padding: 16px;
}

h2 {
  font-size: 16px;
  font-weight: bold;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
}

label {
  width: 60px;
  line-height: 40px;
}
</style>
