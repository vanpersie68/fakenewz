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
    <el-radio
      class="choice-box"
      @change="sendResult"
      v-model="checked"
      v-for="item in questionData.buttons"
      :label="item.text"
      border
    >
      {{ item.text }}
    </el-radio>
  </div>
</template>
<script>
export default {
  props: {
    question: Object,
    index: Number,
  },

  name: 'ButtonRaw',
  data() {
    return {
      questionData: '',
      number: 0,
      checked: '',
      requiredShow: false,
      color: '',
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
      jumpBlockId: 0,
    }
  },
  methods: {
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
      this.generateResultObj()
      this.$emit('updateQuestion', this.resultObj, this.number)
      console.log(this.resultObj)
      this.$emit('updateJumpBlockId', this.jumpBlockId)
    },

    generateResultObj() {
      this.resultObj.question_id = this.questionData.id
      for (let i = 0; i < this.questionData.buttons.length; i++) {
        let flag = false
        if (this.checked === this.questionData.buttons[i].text) {
          flag = true
        }
        if (flag) {
          this.resultObj.response_question_answer[i] = {
            title: this.questionData.buttons[i].text,
            answerText: 'selected',
            answerDecimal: null,
          }

          this.jumpBlockId = this.questionData.buttons[i].jumpBlockId
        } else {
          this.resultObj.response_question_answer[i] = {
            title: this.questionData.buttons[i].text,
            answerText: null,
            answerDecimal: null,
          }
        }
      }
    },

    checkValidity() {
      this.sendResult()
      if (this.questionData.required === true && this.checked.length != 0) {
        console.log(true)
        this.changeColor(true)
        return true
      }
      if (this.questionData.required === false) {
        console.log(true)
        this.changeColor(true)
        return true
      }
      this.changeColor(false)
      return false
    },
  },

  created() {
    this.number = this.index
    this.questionData = this.question
    this.requiredShow = this.questionData.required
    this.checkImg()
    this.sendResult()
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
  .el-radio /deep/ .el-radio__label {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: medium !important;
    white-space: normal;
    word-wrap: break-word;
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
    white-space: normal;
    word-wrap: break-word;
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
    white-space: normal;
    word-wrap: break-word;
  }
}
</style>
