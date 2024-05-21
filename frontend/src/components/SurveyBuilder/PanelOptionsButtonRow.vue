<template>
  <div class="options">
    <h1 class="close-header">{{ $t('pOptionsButtonRow.numButtons') }}</h1>
    <text-box-num
      :value="question.buttons.length.toString()"
      @update="
        (value) =>
          $store.commit('updateButtonList', {
            question: question,
            value: value,
          })
      "
      :key="this.question.buttons.length"
      @increment="insertNewElement($store)"
      @decrement="removeLastElement($store)"
    />
    <line-base class="dark" />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import LineBase from './LineBase.vue'
import ToggleBase from './ToggleBase.vue'
import TextBoxNum from './TextBoxNum.vue'
import store from '../../store/SurveyBuilder.js'

export default {
  name: 'PanelOptionsButtonRow',
  store: store,
  components: {
    LineBase,
    TextBoxNum,
    ToggleBase,
  },
  methods: {
    /**
     * Insert new button into button row and save
     */
    async insertNewElement(store) {
      const resp = await SurveyServices.postButtonRowQuestion(
        this.question.typedata.id,
        {
          buttonText: this.$t('app.buttonDefault'),
        }
      )

      store.commit('insertLastElement', {
        list: this.question.buttons,
        element: { buttonText: this.$t('app.buttonDefault'), ...resp },
      })

      console.log(this.question.buttons, resp)
      // vm.$forceUpdate();
      // this.question.buttons = this.question.buttons
    },
    /**
     * Remove last button from button row and save
     */
    async removeLastElement(store) {
      const temp_id = this.question.buttons.slice(-1)[0].id
      store.commit('removeLastElement', this.question.buttons)

      await SurveyServices.deleteButtonQuestion(this.question.typedata.id, {
        id: String(temp_id),
      })
    },
    async toggleTerminating() {
      store.commit('toggle', { parent: this.question, key: 'terminating' })

      await SurveyServices.patchQuestionType(this.question.id, {
        goToEnd: this.question.terminating,
      })
    },
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
