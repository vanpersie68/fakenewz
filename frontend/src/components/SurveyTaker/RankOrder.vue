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
    <Container @drop="onDrop($event)">
      
      <Draggable v-for="(choice, index) in rankList" :key="choice.id" :draggable="true">
        <div class="draggable-input" type="text" style="word-wrap: normal;">
          {{ index + 1 }}. {{ choice.text }}
        </div>
      </Draggable>

    </Container>
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
import { Container, Draggable } from 'vue-smooth-dnd'
import SurveyServices from '../../services/SurveyServices'

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
      isReordered: false,  
      rankList: this.question.choices,

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
      rankList: this.question.choices,
    }
  },
  components: {
    Container,
    Draggable,
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
    onDrop(v) {
      let ch = [...this.rankList]
      const obj = ch.splice(v.removedIndex, 1)
      ch.splice(v.addedIndex, 0, obj[0])
      ch = ch.map((e, i) => {
        e.order = i + 1
        return e
      })
      this.rankList = ch
      this.checkValidity()
      // ch.forEach((el) => {
      //   console.log(el)
      //   SurveyServices.patchRankOrderQuestion(this.question.typedata.id, {
      //     id: el.id,
      //     order: el.order,
      //     title: el.text
      //   });
      // })
      // this.$set(this.question, 'choices', ch)
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
      let isReordered = false

      for(let i = 0; i < this.rankList.length; i++){
        if(this.rankList[i].order !== this.question.choices[i].order){
          isReordered = true
          break
        }
      }

      if (this.requiredShow && !isReordered) {
        this.changeColor(false)
        return false
      }
      else {
        this.changeColor(true)
        return true
      }
    },
    
    generateResultObj() {
      this.resultObj.question_id = this.questionData.id
      this.resultObj.response_question_answer[0] = {
        title: this.questionData.title,
        answerText: this.rankList || this.question.choices,
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
.draggable-input {
  width: 93%;
  height: auto;
  line-height: 28px;
  margin-bottom: 3px;
  border: 1px solid #333;
  border-radius: 3px;
  padding: 0 10px;
}
</style>

<style>
.el-radio__input {
}
.el-radio__label {
}
</style>
