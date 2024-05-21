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
    <div class="choice-box">
      <div class="scale-labels" style="overflow: hidden">
        <p>{{ questionData.minTitleOn ? questionData.minTitle : '' }}</p>
        <p>{{ questionData.midTitleOn ? questionData.midTitle : '' }}</p>
        <p>{{ questionData.maxTitleOn ? questionData.maxTitle : '' }}</p>
      </div>
      <div class="scale-blocks" style="overflow-y: hidden">
        <div
          v-for="(item, index) in numberShow"
          class="scale-block"
          :key="index"
          :size="btnSize"
          :class="{ isActive: index === s1 }"
          @click="buttonClick(item, index)"
        >
          <p class="item-number">{{ item }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    question: Object,
    index: Number,
  },
  name: 'NumberScale',
  data() {
    return {
      s1: 1000,
      numberShow: [],
      questionData: '',
      number: 0,
      selected: 10000,
      requiredShow: false,
      color: '',
      btnSize: '',
      imgShow: false,
      windowWidth: document.documentElement.clientWidth,

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
  methods: {
    checkImg() {
      if (this.questionData.image === '') {
        this.imgShow = false
      } else {
        this.imgShow = true
      }
    },
    checkBtnSize() {
      if (this.windowWidth > 1130) {
        this.btnSize = ''
      } else if (this.windowWidth < 889) {
        this.btnSize = 'mini'
      } else {
        this.btnSize = 'medium'
      }
    },

    changeColor(color) {
      if (color) {
        this.color = ''
      } else {
        this.color = 'border:1px solid red'
      }
    },
    generateNumShow() {
      let j = 0
      for (
        let i = this.questionData.minNum;
        i < this.questionData.maxNum + 1;
        i += this.questionData.interval
      ) {
        this.numberShow[j++] = i
      }
      console.log(this.numberShow)
    },

    setTitleShow() {
      this.minShow = this.questionData.minTitleOn
      this.maxShow = this.questionData.maxTitleOn
      this.midShow = this.questionData.midTitleOn
      this.requiredShow = this.questionData.required
    },

    buttonClick(item, index) {
      this.selected = item
      this.resultShow = true
      this.sendResult(item)
      this.s1 = index
    },

    sendResult(chooseItem) {
      this.generateResultObj(chooseItem)
      this.$emit('updateQuestion', this.resultObj, this.number)
    },

    generateResultObj(answerText) {
      this.resultObj.question_id = this.questionData.id
      this.resultObj.response_question_answer[0] = {
        title: this.questionData.title,
        answerText: answerText,
        answerDecimal: null,
      }
    },

    checkValidity() {
      if (this.questionData.required === true && this.selected != 10000) {
        console.log(true)
        this.changeColor(true)
        return true
      } else if (this.questionData.required === false) {
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
    this.generateNumShow()
    this.setTitleShow()
    this.checkBtnSize()
    this.checkImg()
    this.sendResult(0)
  },
}
</script>

<style scoped>
.question-box {
  border: 2px solid #eff2f5;
  border-radius: 4px;
  padding: 8px;
  background: white;
  font-family: Arial, Helvetica, sans-serif;
  width: auto;
}

.choice-box {
  width: 98%;
  padding: 8px;
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
}

.isActive {
  border: 1px solid #409eff;
  background-color: #409eff;
  color: #fff;
}

.scale-blocks,
.scale-labels {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  overflow: scroll;
  color: #7f7f7f;
}

.scale-block {
  text-align: center;
  border: 1px solid #bad8fb;
  border-radius: 8px;
  flex-grow: 1;
  justify-content: center;
  display: flex;
}

.scale-block:hover {
  border: 1px solid #409eff;
  background-color: #409eff;
  color: #fff;
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

  .item-number {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    font-weight: bold;
  }

  .scale-blocks,
  .scale-labels {
    color: #7f7f7f;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
  }

  .scale-block {
    margin: 2px;
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
  .item-number {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    font-weight: bold;
  }

  .scale-blocks,
  .scale-labels {
    color: #7f7f7f;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
  }

  .scale-block {
    margin: 2px;
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
  .item-number {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    font-weight: bold;
  }

  .scale-blocks,
  .scale-labels {
    color: #7f7f7f;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
  }

  .scale-block {
    margin: 1px;
  }
}
</style>
