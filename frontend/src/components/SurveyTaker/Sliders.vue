<template>
  <div class="question-box" :style="color">
    <div class="title">
      <h1>
        Q{{ number + 1 }}<span style="color: red" v-show="requiredShow">*</span>
      </h1>
      <p class="title">{{ questionData.title }}</p>
    </div>
    <div style="width: 100%; text-align: center" v-show="imgShow">
      <img :src="questionData.image" alt="" style="width: 60%" />
    </div>
    <el-table
      ref="singleTable"
      :data="tableConfig"
      :span-method="slidersSpanMethod"
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column property="name"> </el-table-column>
      <el-table-column
        v-for="column in columnConfig"
        :key="column.value"
        :property="column.value"
        :label="column.label"
      >
        <template slot-scope="scope">
          <div style="height: 50px">
            <el-slider
              v-model="scope.row.sliderVal"
              :step="question.typedata.grid"
              :min="question.typedata.min"
              :max="question.typedata.max"
              :marks="marks"
              @change="sliderChange($event, scope)"
            ></el-slider>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="showInput" style="width: 100%; text-align: center">
      <el-input
        v-model="otherInputText"
        style="width: 97%"
        @blur="sendResult"
        :placeholder="$t('textBox.yourAnswer')"
      ></el-input>
    </div>
    <span class="tip-box" v-if="oneOrMore === 2"
      ><span style="color: red">Tips:</span> Please select
      {{ this.questionData.textboxMin }} ~
      {{ this.questionData.textboxMax }} choices!</span
    >
  </div>
</template>
<script>
export default {
  props: {
    question: Object,
    index: Number,
  },

  name: 'MultipleChoice',
  data() {
    return {
      questionData: '',
      number: 0,
      checked: [],
      requiredShow: false,
      color: '',
      oneOrMore: 1,
      otherInputText: '',
      showInput: false,
      imgShow: false,

      resultObj: {
        question_id: 0,
        response_question_answer: [
          {
            title: '',
            answerText: null,
            answerDecimal: null,
          },
        ],
      },
    }
  },
  created() {
    this.number = this.index

    this.questionData = this.question
    this.choicesSort(this.questionData)
    console.log(this.questionData)
    this.requiredShow = this.questionData.required
    if (this.questionData.typedata.otherInput) {
      this.questionData.choices.push({
        order: 999,
        text: this.$t('builderQuestion.other'),
        title: this.$t('builderQuestion.other'),
      })
    }
    this.checkOneOrMoreRules()
    this.checkImg()
    this.sendResult()
  },
  computed: {
    marks() {
      const obj = {}
      let min = this.question.typedata.min
      const max = this.question.typedata.max
      const grid = this.question.typedata.grid
      while (min <= max) {
        obj[min] = { label: min }
        min += grid
      }
      return obj
    },
    columnConfig: function () {
      return this.question.typedata.columnConfig
        ? JSON.parse(this.question.typedata.columnConfig)
        : []
    },
    tableConfig: {
      get() {
        return this.question.typedata.tableConfig
          ? JSON.parse(this.question.typedata.tableConfig)
          : []
      },
      set(val) {
        return (this.question.typedata.tableConfig = JSON.parse(val))
      },
    },
  },
  methods: {
    sliderMousedown(e) {
      e.stopPropagation()
    },
    sliderChange(e, s) {
      console.log(e, s)
    },
    slidersSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0) {
        // return [0, 0];
      } else if (columnIndex === 1) {
        return [1, 500]
      }
    },
    checkImg() {
      if (this.questionData.image === '') {
        this.imgShow = false
      } else {
        this.imgShow = true
      }
    },

    choicesSort(questionData) {
      let temp
      for (let i = 1; i < questionData.choices.length; i++) {
        for (let j = 0; j < questionData.choices.length - i; j++) {
          if (
            questionData.choices[j].order > questionData.choices[j + 1].order
          ) {
            temp = questionData.choices[j + 1]
            questionData.choices[j + 1] = questionData.choices[j]
            questionData.choices[j] = temp
          }
        }
      }
    },

    checkOneOrMoreRules() {
      if (this.questionData.multipleAnswers) {
        if (
          this.questionData.textboxMin === 1 &&
          this.questionData.textboxMax === 1
        ) {
          this.oneOrMore = 1
        } else {
          this.oneOrMore = 2
        }
      } else {
        this.oneOrMore = 1
      }
    },

    changeColor(color) {
      if (color) {
        this.color = ''
      } else {
        this.color = 'border:1px solid red'
      }
    },
    sendResult() {
      this.showInput = this.checked === this.$t('builderQuestion.other')
      this.generateResultObj()
      this.$emit('updateQuestion', this.resultObj, this.number)
      this.checkValidity()
    },

    checkValidity() {
      if (this.questionData.required) {
        if (this.checked.length === 0) {
          this.changeColor(false)
          return false
        } else {
          if (this.questionData.multipleAnswers && this.oneOrMore === 2) {
            if (
              this.checked.length >= this.questionData.textboxMin &&
              this.checked.length <= this.questionData.textboxMax
            ) {
              this.changeColor(true)
              return true
            } else {
              this.changeColor(false)
              return false
            }
          } else {
            this.changeColor(true)
            return true
          }
        }
      } else {
        if (this.checked.length === 0) {
          this.changeColor(true)
          return true
        } else {
          if (this.questionData.multipleAnswers && this.oneOrMore === 2) {
            if (
              this.checked.length >= this.questionData.textboxMin &&
              this.checked.length <= this.questionData.textboxMax
            ) {
              this.changeColor(true)
              return true
            } else {
              this.changeColor(false)
              return false
            }
          } else {
            this.changeColor(true)
            return true
          }
        }
      }
    },

    generateResultObj() {
      this.resultObj.question_id = this.questionData.id
      this.resultObj.response_question_answer[0] = {
        title: this.questionData.title,
        answerText: this.tableConfig,
      }
    },
  },
}
</script>

<style scoped>
.question-box {
  border: 2px solid #eff2f5;
  border-radius: 4px;
  background: white;
  padding: 8px;
  width: auto;
}

.tip-box {
  font-size: 13px;
  color: #6e6e6e;
  margin: 8px;
  padding: 8px;
}

.el-slider__marks .el-slider__marks-text:last-of-type {
  /*width: 30px;*/
  width: 100%;
}

@media (min-width: 1130px) {
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    text-align: left;
    margin-right: 8px;
    font-size: 30px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    font-family: Arial, Helvetica, sans-serif;
    font-size: larger;
    font-weight: bold;
    white-space: normal;
    word-wrap: break-word;
  }
  .el-radio /deep/ .el-radio__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: medium !important;
  }

  /deep/ .el-checkbox__input + .el-checkbox__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: medium !important;
  }
}
@media (max-width: 1129px) and (min-width: 890px) {
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    font-size: 25px;
    text-align: left;
    margin-right: 8px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: large;
    font-weight: bold;
  }
  .el-radio /deep/ .el-radio__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 13px !important;
  }

  /deep/ .el-checkbox__input + .el-checkbox__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 13px !important;
  }
}
@media (max-width: 889px) {
  .question-box {
    margin: 2px;
  }
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    font-size: 20px;
    text-align: left;
    margin-right: 8px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: small;
    font-weight: bold;
  }
  .el-radio /deep/ .el-radio__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: smaller !important;
  }

  /deep/ .el-checkbox__input + .el-checkbox__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: smaller !important;
  }
}
</style>
