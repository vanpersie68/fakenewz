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

    <div class="group-wrapper">
      <Container
        class="group-left"
        :should-animate-drop="(src, payload) => true"
        :get-child-payload="(itemIndex) => getChildPayload(itemIndex, 'root')"
        @drop="groupsDropFa(group, $event)"
        :should-accept-drop="(src, payload) => true"
      >
        <p>{{ $t("surveyTaker.Items")}}</p>
        <Draggable
          v-for="item in tableConfig"
          :key="item.name"
          class="question-titles"
        >
          <div class="ques-item">{{ item.name }}</div>
        </Draggable>
      </Container>
      <div class="group-right">
        <Container
          v-for="(group, inx) in columnConfig"
          :key="group.value"
          class="group-item"
          @drop="groupsDrop(group, $event)"
          :should-accept-drop="(src, payload) => true"
          :should-animate-drop="(src, payload) => false"
          :get-child-payload="
            (itemIndex) => getChildPayloadChil(itemIndex, inx, 'chil')
          "
        >
          <p style="text-align: center">{{ group.label }}</p>

          <Draggable v-for="(item, i) in group.children" :key="item.name">
            <div class="ques-item">
              <span class="ques-item-idx">{{ i + 1 }}</span>

              {{ item.name }}
            </div>
          </Draggable>
        </Container>
      </div>
    </div>

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

export default {
  props: {
    question: Object,
    index: Number,
  },
  components: {
    Container,
    Draggable,
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
    columnConfig: {
      get() {
        return this.question.typedata.columnConfig
          ? JSON.parse(this.question.typedata.columnConfig)
          : []
      },
      set(val) {
        return (this.question.typedata.columnConfig = JSON.stringify(val))
      },
    },
    tableConfig: {
      get() {
        let data = this.question.typedata.tableConfig
          ? JSON.parse(this.question.typedata.tableConfig)
          : []
        data = data.filter(
          (el) =>
            !this.columnConfig.some((el2) =>
              el2.children.some((el3) => el3.name === el.name)
            )
        )
        return data
      },
      set(val) {
        return (this.question.typedata.tableConfig = JSON.stringify(val))
      },
    },
  },
  methods: {
    groupsDropFa(e) {
      console.log(e)
    },
    getChildPayload(itemIndex, type) {
      return { ...this.tableConfig[itemIndex - 1], type }
    },
    getChildPayloadChil(itemIndex, inx, type) {
      return {
        ...this.columnConfig[inx].children[itemIndex - 1],
        type,
        delIdx: itemIndex - 1,
      }
    },
    groupsDrop(group, e) {
      console.log(group, e)
      // if()
      if (e.payload.type === 'root') {
        if (e.addedIndex === null) return
        this.columnConfig[
          this.columnConfig.findIndex((el) => el.value === group.value)
        ].children.splice(e.addedIndex - 1, 0, e.payload)
        this.columnConfig = this.columnConfig
        this.sendResult()
        // this.tableConfig.splice(this.tableConfig.findIndex(el => el.name === e.payload.name),1)
        // this.tableConfig = this.tableConfig
      } else {
        if (e.removedIndex !== null) {
          this.columnConfig[
            this.columnConfig.findIndex((el) => el.value === group.value)
          ].children.splice(e.removedIndex - 1, 1)
        }
        if (e.addedIndex !== null) {
          this.columnConfig[
            this.columnConfig.findIndex((el) => el.value === group.value)
          ].children.splice(e.addedIndex - 1, 0, e.payload)
        }

        this.columnConfig = this.columnConfig
        this.sendResult()
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
    const totalItemsInRightBoxes = this.columnConfig.reduce((sum, group) => sum + group.children.length, 0);
    
    if (this.questionData.required) {
      if (totalItemsInRightBoxes === 0) {
        this.changeColor(false);
        return false;
      } else {
        if (this.questionData.multipleAnswers && this.oneOrMore === 2) {
          if (
            totalItemsInRightBoxes >= this.questionData.textboxMin &&
            totalItemsInRightBoxes <= this.questionData.textboxMax
          ) {
            this.changeColor(true);
            return true;
          } else {
            this.changeColor(false);
            return false;
          }
        } else {
          this.changeColor(true);
          return true;
        }
      }
    } else {
      if (totalItemsInRightBoxes === 0) {
        this.changeColor(true);
        return true;
      } else {
        if (this.questionData.multipleAnswers && this.oneOrMore === 2) {
          if (
            totalItemsInRightBoxes >= this.questionData.textboxMin &&
            totalItemsInRightBoxes <= this.questionData.textboxMax
          ) {
            this.changeColor(true);
            return true;
          } else {
            this.changeColor(false);
            return false;
          }
        } else {
          this.changeColor(true);
          return true;
        }
      }
    }
  },
    generateResultObj() {
      this.resultObj.question_id = this.questionData.id
      this.resultObj.response_question_answer[0] = {
        title: this.questionData.title,
        answerText: this.columnConfig,
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
.group-wrapper {
  display: flex;
}
.group-wrapper p {
  text-align: center;
}
.group-left {
  border: 1px solid #ccc;
  width: 180px;
  height: 100%;
  margin-right: 50px;
  border-radius: 5px;
  min-height: 314px;
}
.group-right {
  flex: 1;
}
.group-item {
  border: 1px solid #ccc;
  height: 150px;
  overflow-y: auto;
  margin-bottom: 12px;
  border-radius: 5px;
}
.group-item p {
  text-align: center;
  width: 100%;
}
.ques-item {
  padding: 6px 24px;
}
.ques-item-idx {
  background: #444;
  display: inline-block;
  color: #fff;
  height: 24px;
  border-radius: 12px;
  min-width: 28px;
  text-align: center;
  line-height: 24px;
  margin-right: 12px;
}
</style>

<style>
.el-radio__input {
}
.el-radio__label {
}
</style>
