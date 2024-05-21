<template>
  <div class="options">
    <h1>{{ $t('pOptionsNumScale.scaleSettings') }}</h1>
    <line-base class="light" />
    <h1 class="close-header">{{ $t('pOptionsNumScale.minValue') }}</h1>
    <text-box-num
      :value="question.minNum.toString()"
      @update="(input) => updateMinNum(input, $store)"
      @increment="(input) => incrementMinNum(input, $store)"
      @decrement="(input) => decrementMinNum(input, $store)"
    />
    <line-base class="light" />
    <h1 class="close-header">{{ $t('pOptionsNumScale.maxValue') }}</h1>
    <text-box-num
      :value="question.maxNum.toString()"
      @update="(input) => updateMaxNum(input, $store)"
      @increment="(input) => incrementMaxNum(input, $store)"
      @decrement="(input) => decrementMaxNum(input, $store)"
    />
    <line-base class="light" />
    <h1 class="close-header">{{ $t('pOptionsNumScale.stepValue') }}</h1>
    <text-box-num
      :value="question.interval.toString()"
      @update="(input) => updateIntervalNum(input, $store)"
      @increment="(input) => incrementIntervalNum(input, $store)"
      @decrement="(input) => decrementIntervalNum(input, $store)"
    />
    <line-base class="dark" />
    <h1>{{ $t('pOptionsNumScale.scaleLabels') }}</h1>
    <line-base class="light" />
    <div class="text-with-button">
      <h2>{{ $t('pOptionsNumScale.minLabelShow') }}</h2>
      <toggle-base
        :toggled="question.minTitleOn"
        @handleToggle="toggleMinTitleOn($store)"
      ></toggle-base>
    </div>
    <div class="text-with-button">
      <h2>{{ $t('pOptionsNumScale.midLabelShow') }}</h2>
      <toggle-base
        :toggled="question.midTitleOn"
        @handleToggle="toggleMidTitleOn($store)"
      ></toggle-base>
    </div>
    <div class="text-with-button">
      <h2>{{ $t('pOptionsNumScale.maxLabelShow') }}</h2>
      <toggle-base
        :toggled="question.maxTitleOn"
        @handleToggle="toggleMaxTitleOn($store)"
      ></toggle-base>
    </div>
    <line-base class="dark" />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import LineBase from './LineBase.vue'
import TextBoxNum from './TextBoxNum.vue'
import ToggleBase from './ToggleBase.vue'

export default {
  name: 'PanelOptionsNumberScale',
  components: {
    LineBase,
    TextBoxNum,
    ToggleBase,
  },
  props: {
    question: Object,
  },
  methods: {
    async toggleMinTitleOn(store) {
      console.log('toggleMinTitleOn')
      store.commit('toggle', { parent: this.question, key: 'minTitleOn' })
      if (this.question.minTitleOn === false) {
        store.commit('toggleTitle', { parent: this.question, key: 'minTitle' })
      }
      await SurveyServices.patchNumberScale(this.question.id, {
        minTitleOn: this.question.minTitleOn,
      })
    },

    async toggleMidTitleOn(store) {
      console.log('toggleMidTitleOn')
      store.commit('toggle', { parent: this.question, key: 'midTitleOn' })
      if (this.question.midTitleOn === false) {
        store.commit('toggleTitle', { parent: this.question, key: 'midTitle' })
      }
      await SurveyServices.patchNumberScale(this.question.id, {
        midTitleOn: this.question.midTitleOn,
      })
    },

    async toggleMaxTitleOn(store) {
      console.log('toggleMaxTitleOn')
      store.commit('toggle', { parent: this.question, key: 'maxTitleOn' })
      if (this.question.maxTitleOn === false) {
        store.commit('toggleTitle', { parent: this.question, key: 'maxTitle' })
      }
      await SurveyServices.patchNumberScale(this.question.id, {
        maxTitleOn: this.question.maxTitleOn,
      })
    },

    async updateMinNum(value, store) {
      if (value < this.question.maxNum) {
        store.commit('updateValue', {
          parent: this.question,
          key: 'minNum',
          value: value,
        })

        await SurveyServices.patchQuestionType(this.question.id, {
          numberMin: value,
        })
      }
    },
    async incrementMinNum(value, store) {
      if (this.question.minNum <= this.question.maxNum - 1) {
        store.commit('updateValue', {
          parent: this.question,
          key: 'minNum',
          value: parseInt(this.question.minNum) + 1,
        })

        await SurveyServices.patchQuestionType(this.question.id, {
          numberMin: parseInt(this.question.minNum),
        })
      }
    },
    async decrementMinNum(value, store) {
      store.commit('updateValue', {
        parent: this.question,
        key: 'minNum',
        value: parseInt(this.question.minNum) - 1,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        numberMin: parseInt(this.question.minNum),
      })
    },
    async updateMaxNum(value, store) {
      if (value > this.question.minNum) {
        store.commit('updateValue', {
          parent: this.question,
          key: 'maxNum',
          value: value,
        })

        await SurveyServices.patchQuestionType(this.question.id, {
          numberMax: value,
        })
      }
    },
    async decrementMaxNum(value, store) {
      if (this.question.maxNum > this.question.minNum + 1) {
        store.commit('updateValue', {
          parent: this.question,
          key: 'maxNum',
          value: parseInt(this.question.maxNum) - 1,
        })

        await SurveyServices.patchQuestionType(this.question.id, {
          numberMax: parseInt(this.question.maxNum),
        })
      }
    },
    async incrementMaxNum(value, store) {
      store.commit('updateValue', {
        parent: this.question,
        key: 'maxNum',
        value: parseInt(this.question.maxNum) + 1,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        numberMax: parseInt(this.question.maxNum),
      })
    },
    async updateIntervalNum(value, store) {
      store.commit('updateValue', {
        parent: this.question,
        key: 'interval',
        value: value,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        interval: value,
      })
    },
    async incrementIntervalNum(value, store) {
      store.commit('updateValue', {
        parent: this.question,
        key: 'interval',
        value: parseInt(this.question.interval) + 1,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        interval: parseInt(this.question.interval),
      })
    },
    async decrementIntervalNum(value, store) {
      if (this.question.interval > 1) {
        store.commit('updateValue', {
          parent: this.question,
          key: 'interval',
          value: parseInt(this.question.interval) - 1,
        })
      }

      await SurveyServices.patchQuestionType(this.question.id, {
        interval: parseInt(this.question.interval),
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
