<template>
  <div class="options">
    <h1 class="close-header">{{ $t('pOptionsMC.numOptions') }}</h1>
    <!-- This is the actual number field -->
    <text-box-num
      :value="question.choices.length.toString()"
      :key="question.choices.length"
      @update="
        (value) =>
          $store.commit('updateMultiList', { question: question, value: value })
      "
      @increment="insertNewElement($store)"
      @decrement="removeLastElement($store)"
    />
    <line-base class="dark" v-if="!question.multipleAnswers" />
    <div class="text-with-button" v-if="!question.multipleAnswers">
      <!-- The answer required toggle -->
      <h2>{{ $t('pOptionsMC.otherInput') }}</h2>
      <toggle-base
        :toggled="question.otherInput"
        @handleToggle="toggleMultipleOtherInput($store)"
      ></toggle-base>
    </div>
    <line-base class="dark" />
    <div class="text-with-button">
      <!-- The answer required toggle -->
      <h2>{{ $t('pOptionsMC.allowMultiple') }}</h2>
      <toggle-base
        :toggled="question.multipleAnswers"
        @handleToggle="toggleMultipleAnswers($store)"
      ></toggle-base>
    </div>
    <div v-if="question.multipleAnswers">
      <!-- This is for multiple answers -->
      <line-base class="light" />
      <h1 class="close-header">{{ $t('pOptionsMC.setMinimum') }}</h1>
      <text-box-num
        :value="
          question.textboxMin != null ? question.textboxMin.toString() : null
        "
        :key="question.textboxMin"
        @update="(value) => updateMultiChoiceMinValue($store, 'update', value)"
        @increment="updateMultiChoiceMinValue($store, 'inc')"
        @decrement="updateMultiChoiceMinValue($store, 'dec')"
      />
      <line-base class="light" />
      <h1 class="close-header">{{ $t('pOptionsMC.setMaximum') }}</h1>
      <text-box-num
        :value="
          question.textboxMax != null ? question.textboxMax.toString() : null
        "
        :key="question.textboxMax"
        @update="(value) => updateMultiChoiceMaxValue($store, 'update', value)"
        @increment="updateMultiChoiceMaxValue($store, 'inc')"
        @decrement="updateMultiChoiceMaxValue($store, 'dec')"
      />
    </div>
    <line-base class="dark" />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import LineBase from './LineBase.vue'
import ToggleBase from './ToggleBase.vue'
import TextBoxNum from './TextBoxNum.vue'

export default {
  name: 'PanelOptionsMultipleChoice',
  components: {
    ToggleBase,
    LineBase,
    TextBoxNum,
  },
  methods: {
    /**
     * Insert a new choice for multiple choice question and save
     */
    async insertNewElement(store) {
      const resp = await SurveyServices.postMultiChoiceQuestion(
        this.question.typedata.id,
        {
          order: String(this.question.choices.length + 1),
          title: this.$t('app.MCDefault'),
        }
      )
      console.log(resp)
      store.commit('insertLastElement', {
        list: this.question.choices,
        element: { text: this.$t('app.MCDefault'), ...resp },
      })
    },
    /**
     * Remove last choice from multiple choice question and save
     */
    async removeLastElement(store) {
      const temp_id = this.question.choices.slice(-1)[0].id
      store.commit('removeLastElement', this.question.choices)

      await SurveyServices.deleteMultiChoiceQuestion(
        this.question.typedata.id,
        { id: String(temp_id) }
      )
    },
    /**
     * toggle the multiple choice button
     */
    async toggleMultipleAnswers(store) {
      this.question.otherInput = false
      store.commit('toggle', {
        parent: this.question,
        key: 'multipleAnswers',
      })
      await SurveyServices.patchMultiChoiceAnswers(this.question.typedata.id, {
        multipleAnswers: this.question.multipleAnswers,
        otherInput: this.question.otherInput,
      })
    },
    async toggleMultipleOtherInput(store) {
      store.commit('toggle', {
        parent: this.question,
        key: 'otherInput',
      })
      await SurveyServices.patchMultiChoiceAnswers(this.question.typedata.id, {
        otherInput: this.question.otherInput,
      })
    },
    /**
     new  update to the textboxmin
     */
    async updateMultiChoiceMinValue(store, flag, value) {
      if (flag == 'update') {
        if (value < 0 || value > this.question.textboxMax) {
          await this.$alert(
            this.$t(
              'app.Minimum Answers Permitted must between 0 and Maximum Answers Permitted '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else {
          this.question.textboxMin = value
        }
      }
      if (flag == 'inc') {
        if (parseInt(this.question.textboxMin) + 1 > this.question.textboxMax) {
          await this.$alert(
            this.$t(
              'app.Minimum Answers Permitted must less than Maximum Answers Permitted '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else {
          this.question.textboxMin = parseInt(this.question.textboxMin) + 1
        }
      }
      if (flag == 'dec') {
        if (parseInt(this.question.textboxMin) - 1 < 0) {
          await this.$alert(
            this.$t('app.Minimum Answers Permitted must more than 0 '),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else {
          this.question.textboxMin = parseInt(this.question.textboxMin) - 1
        }
      }
      await SurveyServices.patchMultiChoiceAnswers(this.question.typedata.id, {
        textboxMin: this.question.textboxMin,
      })
    },
    /**
     * //new update to the textboxmax
     */
    async updateMultiChoiceMaxValue(store, flag, value) {
      if (flag == 'update') {
        if (
          value < this.question.textboxMin ||
          value > this.question.choices.length
        ) {
          await this.$alert(
            this.$t(
              'app.Maximum Answers Permitted must between Minimum Answers and Number of Options'
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else {
          this.question.textboxMax = value
        }
      }
      if (flag == 'inc') {
        if (
          parseInt(this.question.textboxMax + 1) > this.question.choices.length
        ) {
          await this.$alert(
            this.$t(
              'app.Maximum Answers Permitted must less than Number of Options '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else {
          this.question.textboxMax = parseInt(this.question.textboxMax + 1)
        }
      }
      if (flag == 'dec') {
        if (parseInt(this.question.textboxMax) - 1 < this.question.textboxMin) {
          await this.$alert(
            this.$t(
              'app.Maximum Answers Permitted must more than Minimum Answers '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else this.question.textboxMax = parseInt(this.question.textboxMax) - 1
      }
      await SurveyServices.patchMultiChoiceAnswers(this.question.typedata.id, {
        textboxMax: this.question.textboxMax,
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
