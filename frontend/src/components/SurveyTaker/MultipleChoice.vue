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
    <el-checkbox-group
      v-model="checked"
      v-if="oneOrMore === 2"
      @change="sendResult"
    >
      <el-checkbox
        class="choice-box"
        v-for="item in this.questionData.choices"
        :key="item.id"
        :label="item.text"
        border
      >
        {{ item.text }}
      </el-checkbox>
    </el-checkbox-group>

    <el-radio
      class="choice-box"
      v-else-if="oneOrMore === 1"
      @change="sendResult"
      v-model="checked"
      v-for="item in this.questionData.choices"
      :label="item.text"
      border
    >
      {{ item.text }}
    </el-radio>
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
  methods: {
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
      if (this.oneOrMore === 1) {
        for (let i = 0; i < this.questionData.choices.length; i++) {
          let flag = false
          if (this.checked === this.questionData.choices[i].text) {
            flag = true
          }
          if (flag) {
            if (
              this.checked === this.$t('builderQuestion.other') &&
              this.checked === this.questionData.choices[i].text
            ) {
              this.resultObj.response_question_answer[i] = {
                title: this.questionData.choices[i].text,
                answerText: this.otherInputText,
                answerDecimal: null,
              }
            } else {
              this.resultObj.response_question_answer[i] = {
                title: this.questionData.choices[i].text,
                answerText: 'selected',
                answerDecimal: null,
              }
            }
          } else {
            this.resultObj.response_question_answer[i] = {
              title: this.questionData.choices[i].text,
              answerText: null,
              answerDecimal: null,
            }
          }
        }
      } else if (this.oneOrMore === 2) {
        for (let i = 0; i < this.questionData.choices.length; i++) {
          let flag = false
          for (let j = 0; j < this.checked.length; j++) {
            if (this.checked[j] === this.questionData.choices[i].text) {
              flag = true
            }
          }
          if (flag) {
            this.resultObj.response_question_answer[i] = {
              title: this.questionData.choices[i].text,
              answerText: 'selected',
              answerDecimal: null,
            }
          } else {
            this.resultObj.response_question_answer[i] = {
              title: this.questionData.choices[i].text,
              answerText: null,
              answerDecimal: null,
            }
          }
        }
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

.choice-box {
  height: auto;
  border-radius: 4px;
  padding: 8px;
  margin: 8px;
  display: block;
  white-space: normal;
  word-wrap: break-word;
}

.choice-box:hover {
  border: 1px solid #409eff;
}
.tip-box {
  font-size: 13px;
  color: #6e6e6e;
  margin: 8px;
  padding: 8px;
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

<style>
.el-radio__input {
}
.el-radio__label {
}
</style>
