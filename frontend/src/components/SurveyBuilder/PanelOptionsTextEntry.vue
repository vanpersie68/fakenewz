<template>
  <div class="options">
    <div class="text-with-button">
      <!--Validate Answer-->
      <h2>{{ $t('pOptionsTextEntry.validateAnswer') }}</h2>
      <!--new toggleValidationQuestion-->
      <toggle-base
        :toggled="question.validate"
        @handleToggle="toggleValidationQuestion($store)"
      ></toggle-base>
    </div>
    <div v-if="question.validate">
      <line-base class="light" />
      <h1 class="close-header">{{ $t('pOptionsTextEntry.answerType') }}</h1>
      <dropdown-base
        :options="['Text', 'Integer', 'Decimal', 'Date']"
        :currentType="question.ansType"
        @input="handleTextAnswerType"
        class="secondary-drop"
      />
      <div v-if="question.ansType !== 'Date'">
        <line-base class="light" />
        <h1 v-if="question.ansType === 'Text'" class="close-header">
          {{ $t('pOptionsTextEntry.minCharLength') }}
        </h1>
        <h1 v-else-if="question.ansType === 'Integer'" class="close-header">
          {{ $t('pOptionsTextEntry.intLowerBound') }}
        </h1>
        <h1 v-else class="close-header">
          {{ $t('pOptionsTextEntry.decLowerBound') }}
        </h1>
        <text-box-num
          :placeholder="$t('pOptionsTextEntry.minPlaceholder')"
          :value="
            question.textboxMin != null ? question.textboxMin.toString() : null
          "
          :key="question.textboxMin"
          @update="(value) => updateTextboxMinValue($store, 'update', value)"
          @increment="updateTextboxMinValue($store, 'inc')"
          @decrement="updateTextboxMinValue($store, 'dec')"
        />
        <line-base class="light" />
        <h1 v-if="question.ansType === 'Text'" class="close-header">
          {{ $t('pOptionsTextEntry.maxCharLength') }}
        </h1>
        <h1 v-else-if="question.ansType === 'Integer'" class="close-header">
          {{ $t('pOptionsTextEntry.intUpperBound') }}
        </h1>
        <h1 v-else-if="question.ansType === 'Decimal'" class="close-header">
          {{ $t('pOptionsTextEntry.decUpperBound') }}
        </h1>
        <text-box-num
          :placeholder="$t('pOptionsTextEntry.maxPlaceholder')"
          :value="
            question.textboxMax != null ? question.textboxMax.toString() : null
          "
          :key="question.textboxMax"
          @update="(value) => updateTextboxMaxValue($store, 'update', value)"
          @increment="updateTextboxMaxValue($store, 'inc')"
          @decrement="updateTextboxMaxValue($store, 'dec')"
        />
      </div>
      <line-base class="dark" />
    </div>
  </div>
</template>

<script>
import LineBase from './LineBase.vue'
import ToggleBase from './ToggleBase.vue'
import TextBoxNum from './TextBoxNum.vue'
import DropdownBase from './DropdownBase.vue'
import store from '../../store/SurveyBuilder.js'
import SurveyServices from '@/services/SurveyServices'

export default {
  name: 'PanelOptionsTextEntry',
  store: store,
  components: {
    ToggleBase,
    LineBase,
    TextBoxNum,
    DropdownBase,
  },
  props: {
    question: Object,
  },
  methods: {
    /**
     * Handle text entry question answer type being changed in dropdown
     * @param data - data provided by dropdown
     */
    handleTextAnswerType(data) {
      store.commit('handleTextAnswerType', {
        question: this.question,
        ansType: data,
      })
      SurveyServices.patchTextAnswerType(this.question.id, { ansType: data })
    },
    async toggleValidationQuestion(store) {
      //This is new method to update validation
      store.commit('toggle', {
        parent: this.question,
        key: 'validate',
      })

      await SurveyServices.patchTextAnswerType(this.question.id, {
        validate: this.question.validate,
      })
    },
    async updateTextboxMinValue(store, flag, value) {
      //new  update to the textboxmin
      if (flag == 'update') {
        if (value > this.question.textboxMax) {
          await this.$alert(
            this.$t(
              'app.Maximum Answers Permitted must more than Minimum Answers '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else this.question.textboxMin = value
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
        } else this.question.textboxMin = parseInt(this.question.textboxMin) + 1
      }

      if (flag == 'dec') {
        this.question.textboxMin = parseInt(this.question.textboxMin) - 1
      }

      await SurveyServices.patchTextAnswerType(this.question.id, {
        textboxMin: this.question.textboxMin,
      })
    },
    async updateTextboxMaxValue(store, flag, value) {
      //new update to the textboxmax
      if (flag == 'update') {
        if (value < this.question.textboxMin) {
          await this.$alert(
            this.$t(
              'app.Maximum Answers Permitted must more than Minimum Answers '
            ),
            this.$t('app.Warning'),
            {
              confirmButtonText: this.$t('app.Confirm'),
            }
          )
        } else this.question.textboxMax = value
      }

      if (flag == 'inc') {
        this.question.textboxMax = parseInt(this.question.textboxMax + 1)
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

      await SurveyServices.patchTextAnswerType(this.question.id, {
        textboxMax: this.question.textboxMax,
      })
    },
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
