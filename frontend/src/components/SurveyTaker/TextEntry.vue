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

    <div class="choice-box" v-show="textShow">
      <el-input
        type="textarea"
        :rows="2"
        :placeholder="questionData.query"
        v-model="answerText"
        @blur="sendResult"
        show-word-limit
      >
      </el-input>
    </div>

    <div class="choice-box" v-show="integerShow">
      <el-input
        type="textarea"
        :rows="2"
        :placeholder="questionData.query"
        oninput="value=value.replace(/[^0-9.]/g,'')"
        v-model="answerDecimal"
        @blur="sendResult"
        show-word-limit
      >
      </el-input>
    </div>

    <div class="choice-box" v-show="decimalShow">
      <el-input-number
        :precision="2"
        :placeholder="questionData.query"
        v-model="answerDecimal"
        @change="sendResult"
      >
      </el-input-number>
    </div>
    <div class="choice-box" v-show="dateShow">
      <el-date-picker
        v-model="answerText"
        :placeholder="questionData.query"
        type="date"
        @change="sendResult"
        value-format="dd/MM/yyyy"
        format="dd/MM/yyyy"
      ></el-date-picker>
    </div>
    <span class="tip-box" v-if="this.questionData.validate === true">
      <span v-if="this.questionData.ansType === 'Text'"
        ><span style="color: red">Tips:</span> Please input
        {{ this.questionData.textboxMin }} ~
        {{ this.questionData.textboxMax }} characters!</span
      >
      <span v-if="this.questionData.ansType === 'Integer'"
        ><span style="color: red">Tips:</span> Please input
        {{ this.questionData.textboxMin }} ~
        {{ this.questionData.textboxMax }} integers!</span
      >
      <span v-if="this.questionData.ansType === 'Decimal'"
        ><span style="color: red">Tips:</span> Please input
        {{ this.questionData.textboxMin }} ~
        {{ this.questionData.textboxMax }} decimals!</span
      >
    </span>
  </div>
</template>

<script>
export default {
  props: {
    question: Object,
    index: Number,
  },
  name: 'TextEntry',
  data() {
    return {
      questionData: '',
      number: 0,
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
      textShow: false,
      integerShow: false,
      dateShow: false,
      decimalShow: false,
      requiredShow: false,
      imgShow: false,
      answerText: '',
      answerDecimal: null,
      color: '',
    }
  },
  methods: {
    checkType() {
      if (this.questionData.ansType === 'Text') {
        this.textShow = true
      }
      if (this.questionData.ansType === 'Integer') {
        this.integerShow = true
      }
      if (this.questionData.ansType === 'Decimal') {
        this.decimalShow = true
      }
      if (this.questionData.ansType === 'Date') {
        this.dateShow = true
      }
    },

    checkImg() {
      if (this.questionData.image === '') {
        this.imgShow = false
      } else {
        this.imgShow = true
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
      this.checkValidity()
      this.generateResultObj()
      this.$emit('updateQuestion', this.resultObj, this.number)
      console.log(this.resultObj)
    },
    generateResultObj() {
      this.resultObj.question_id = this.questionData.id
      this.resultObj.response_question_answer[0] = {
        title: this.questionData.title,
        answerText: this.answerText,
        answerDecimal: this.answerDecimal,
      }
    },
    checkValidity() {
      if (this.questionData.required === true) {
        if (this.answerText.length != 0 || this.answerDecimal != 0) {
          if (this.questionData.validate == true) {
            if (this.questionData.ansType === 'Text') {
              if (
                this.answerText.length >= this.questionData.textboxMin &&
                this.answerText.length <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }

            if (this.questionData.ansType === 'Integer') {
              if (
                this.answerDecimal >= this.questionData.textboxMin &&
                this.answerDecimal <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }

            if (this.questionData.ansType === 'Decimal') {
              if (
                this.answerDecimal >= this.questionData.textboxMin &&
                this.answerDecimal <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }
            if (this.questionData.ansType === 'Date') {
              this.changeColor(true)
              return true
            }
          } else {
            this.changeColor(true)
            return true
          }
        } else {
          this.changeColor(false)
          return false
        }
      } else if (this.questionData.required === false) {
        if (this.answerText.length != 0 || this.answerDecimal != 0) {
          if (this.questionData.validate == true) {
            if (this.questionData.ansType === 'Text') {
              if (
                this.answerText.length >= this.questionData.textboxMin &&
                this.answerText.length <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }

            if (this.questionData.ansType === 'Integer') {
              if (
                this.answerDecimal >= this.questionData.textboxMin &&
                this.answerDecimal <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }

            if (this.questionData.ansType === 'Decimal') {
              if (
                this.answerDecimal >= this.questionData.textboxMin &&
                this.answerDecimal <= this.questionData.textboxMax
              ) {
                this.changeColor(true)
                return true
              } else {
                this.changeColor(false)
                return false
              }
            }
            if (this.questionData.ansType === 'Date') {
              this.changeColor(true)
              return true
            }
          } else {
            this.changeColor(true)
            return true
          }
        } else {
          this.changeColor(true)
          return true
        }
      }
    },
  },

  created() {
    this.number = this.index
    this.questionData = this.question
    this.requiredShow = this.questionData.required
    this.checkType()
    this.checkImg()
    this.sendResult()
    console.log(this.questionData)
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
  border-radius: 4px;
  padding: 8px;
  margin: 8px;
  display: block;
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
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: larger;
    font-weight: bold;
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
}
</style>
