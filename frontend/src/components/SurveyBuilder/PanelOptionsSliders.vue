<template>
  <div class="options">
    <h1 class="close-header">{{ $t('pOptionsSliders.Number of statements') }}</h1>
    <!-- This is the actual number field -->
    <text-box-num
      :value="tableConfig.length.toString()"
      :key="tableConfig.length"
      @update="
        (value) =>
          $store.commit('updateMultiList1', {
            question: question,
            value: value,
          })
      "
      @increment="insertTableConfig($store)"
      @decrement="removeTableConfig($store)"
    />
    <line-base class="dark" />

    <h1 class="close-header">{{ $t('pOptionsSliders.Number of scale points') }}</h1>
    <!-- This is the actual number field -->
    <text-box-num
      :value="columnConfig.length.toString()"
      :key="columnConfig.length"
      @update="
        (value) =>
          $store.commit('updateMultiList1', {
            question: question,
            value: value,
          })
      "
      @increment="insertColumnConfig($store)"
      @decrement="removeColumnConfig($store)"
    />
    <line-base class="dark" />
    <h1 class="close-header">{{ $t('pOptionsSliders.Scale points')}}</h1>
    <div style="padding: 12px; display: flex">
      <div>
        <label for="">{{ $t('pOptionsSliders.Min') }}</label>
        <el-input-number
          @input="saveConfig"
          controls-position="right"
          v-model="question.typedata.min"
          style="width: 130px"
          type="number"
        />
      </div>
      <div>
        <label for="">{{ $t('pOptionsSliders.Max') }}</label>
        <el-input-number
          @input="saveConfig"
          controls-position="right"
          v-model="question.typedata.max"
          style="width: 130px"
          type="number"
        />
      </div>
    </div>
    <line-base class="dark" />
    <h1 class="close-header">{{ $t('pOptionsSliders.Grid lines') }}</h1>
    <div style="padding: 12px; display: flex">
      <div>
        <div>
          <label for="">{{ $t('pOptionsSliders.Grid') }}</label>
        </div>
        <el-input-number
          @input="saveConfig"
          v-model="question.typedata.grid"
          type="number"
        />
      </div>
    </div>

    <line-base class="dark" />

    <h1 class="close-header">{{ $t('pOptionsSliders.Set columns') }}</h1>
    <div style="padding: 12px">
      <div v-for="(column, index) in columnConfigData" :key="index">
        <el-input v-model="column.label"></el-input>
      </div>
      <el-button
        type="primary"
        style="margin-top: 12px"
        @click="saveColumnConfigData"
        >Save</el-button
      >
    </div>

    <line-base class="dark" />
    <h1 class="close-header">{{ $t('pOptionsSliders.Set statements') }}</h1>
    <div style="padding: 12px">
      <div v-for="(data, index) in tableConfigData" :key="index">
        <el-input v-model="data.name"></el-input>
      </div>
      <el-button
        type="primary"
        style="margin-top: 12px"
        @click="saveTableConfigData"
        >Save</el-button
      >
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
  data() {
    return {
      columnConfigData: this.question.typedata.columnConfig
        ? JSON.parse(this.question.typedata.columnConfig)
        : [],
      tableConfigData: this.question.typedata.tableConfig
        ? JSON.parse(this.question.typedata.tableConfig)
        : [],
    }
  },
  watch: {
    'question.typedata.columnConfig'(a, b) {
      this.columnConfigData = a ? JSON.parse(a) : []
    },
    'question.typedata.tableConfig'(a, b) {
      this.tableConfigData = a ? JSON.parse(a) : []
    },
  },
  computed: {
    columnConfig: {
      get: function () {
        return this.question.typedata.columnConfig
          ? JSON.parse(this.question.typedata.columnConfig)
          : []
      },
      set(val) {
        console.log(val)
      },
    },
    tableConfig: function () {
      return this.question.typedata.tableConfig
        ? JSON.parse(this.question.typedata.tableConfig)
        : []
    },
  },
  methods: {
    async saveConfig() {
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        ...this.question.typedata,
      })
    },
    async saveTableConfigData() {
      const newArr = JSON.stringify(this.tableConfigData)
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        tableConfig: newArr,
      })
      this.question.typedata.tableConfig = newArr
      // this.tableConfigData = this.question.typedata.tableConfig ? JSON.parse(this.question.typedata.tableConfig) : []
    },
    async saveColumnConfigData() {
      const newArr = JSON.stringify(this.columnConfigData)
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        columnConfig: newArr,
      })
      this.question.typedata.columnConfig = newArr
      // this.columnConfigData = this.question.typedata.columnConfig ? JSON.parse(this.question.typedata.columnConfig) : []
    },
    /**
     * Insert a new choice for multiple choice question and save
     */

    async insertTableConfig(store) {
      const newArr = JSON.stringify([
        ...this.tableConfig,
        { name: 'Default' + (this.tableConfig.length + 1) },
      ])
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        tableConfig: newArr,
      })
      this.question.typedata.tableConfig = newArr
      // this.tableConfigData = this.question.typedata.tableConfig ? JSON.parse(this.question.typedata.tableConfig) : []
    },
    async insertColumnConfig(store) {
      const newArr = JSON.stringify([
        ...this.columnConfig,
        {
          label: 'Default' + (this.columnConfig.length + 1),
          value: 'Default' + (this.columnConfig.length + 1),
        },
      ])
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        columnConfig: newArr,
      })
      this.question.typedata.columnConfig = newArr
      // this.columnConfigData = this.question.typedata.columnConfig ? JSON.parse(this.question.typedata.columnConfig) : []
    },
    /**
     * Remove last choice from multiple choice question and save
     */
    async removeTableConfig(store) {
      const newArr = JSON.stringify([...this.tableConfig].slice(0, -1))
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        tableConfig: newArr,
      })
      this.question.typedata.tableConfig = newArr
    },
    async removeColumnConfig(store) {
      const newArr = JSON.stringify([...this.columnConfig].slice(0, -1))
      await SurveyServices.patchSlidersQuestion({
        id: this.question.typedata.id,
        columnConfig: newArr,
      })
      this.question.typedata.columnConfig = newArr
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
      await SurveyServices.patchSlidersAnswers(this.question.typedata.id, {
        multipleAnswers: this.question.multipleAnswers,
        otherInput: this.question.otherInput,
      })
    },
    async toggleMultipleOtherInput(store) {
      store.commit('toggle', {
        parent: this.question,
        key: 'otherInput',
      })
      await SurveyServices.patchSlidersAnswers(this.question.typedata.id, {
        otherInput: this.question.otherInput,
      })
    },
    /**
     new  update to the textboxmin
     */
    async updateSlidersMinValue(store, flag, value) {
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
      await SurveyServices.patchSlidersAnswers(this.question.typedata.id, {
        textboxMin: this.question.textboxMin,
      })
    },
    /**
     * //new update to the textboxmax
     */
    async updateSlidersMaxValue(store, flag, value) {
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
      await SurveyServices.patchSlidersAnswers(this.question.typedata.id, {
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
