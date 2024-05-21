<template>
  <div class="question-box" :style="color">
    <div class="title" style="margin-left: 10%">
      <h1 class="questionNumber">Q{{ index + 1 }} {{ questionData.type }}</h1>
      <h1 style="color: red" v-show="requiredShow">*</h1>
      <p style="font-size: large; font-weight: bold">
        {{ questionData.title }}
      </p>
    </div>
    <div class="newspost">
      <PostTwitterReadOnlyResult
        @updateAnswer="getData"
        @changeValue="changeValue"
        :question="questionData"
      />
    </div>

    <div class="wordSelection">
      <el-carousel
        style="width: 400px"
        height="200px"
        :interval="5000"
        arrow="always"
      >
        <el-carousel-item
          v-for="item in this.questionData.comments"
          style="
            background-color: transparent;
            text-align: center;
            display: table;
            word-break: break-word;
          "
          :key="item"
        >
          <span style="display: table-cell; vertical-align: middle">{{
            item
          }}</span>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="random">
      <button class="action-btn" @click="randomSelection">
        {{ $t('surveyStatistic.randomAnswers') }}
      </button>
      <button class="last-btn" @click="lastSelection">
        {{ $t('surveyStatistic.lastFiveAnswers') }}
      </button>
    </div>
  </div>
</template>

<script>
import PostTwitterReadOnlyResult from './PostTwitterReadOnlyResult'
import PostFacebookReadOnlyResult from './PostFacebookReadOnlyResult'
import SurveyServices from '../../services/SurveyServices'

export default {
  props: {
    question: Object,
    index: Number,
  },
  name: 'NewsPostResult',
  components: {
    PostTwitterReadOnlyResult,
    PostFacebookReadOnlyResult,
  },
  data() {
    return {
      questionData: '',
      number: 0,
      replyOn: true,
      addOn1: false,
      addOn2: false,
      requiredShow: false,
      color: '',
      resultObj: {
        question_id: 0,
        response_question_answer: [
          {
            title: '',
            answerText: null,
            answerDecimal: 0,
          },
        ],
      },
    }
  },
  created() {
    // function sentenceAdjust(str) {
    //   let stringToAdd = " \n ";
    //   for (let index = 20; index < str.length; index += 20) {
    //     str = str.substring(0, index) + stringToAdd + str.substring(index, str.length);
    //   }
    //   return str;
    // }
    //
    // function changeComments(arr) {
    //   for (let i = 0; i < arr.length; i++) {
    //     arr[i] = sentenceAdjust(arr[i]);
    //   }
    //   console.log(arr)
    //   return arr;
    // }

    this.number = this.index
    this.questionData = this.question

    // this.questionData.comments = changeComments(this.question.comments);
    this.requiredShow = this.questionData.required
    console.log('this.questionData comments', this.questionData.comments)
    this.sendResult()
  },
  methods: {
    async randomSelection() {
      let value = await SurveyServices.getRandomFiveResults(
        this.question.question_id
      )
      if (this.replyOn === true) {
        this.questionData.comments = value.comments
      } else if (this.addOn1 === true) {
        this.questionData.comments = value.addon1
      } else {
        this.questionData.comments = value.addon2
      }
    },
    async lastSelection() {
      let value = await SurveyServices.getLastFiveResults(
        this.question.question_id
      )
      if (this.replyOn === true) {
        this.questionData.comments = value.comments
      } else if (this.addOn1 === true) {
        this.questionData.comments = value.addon1
      } else {
        this.questionData.comments = value.addon2
      }
    },
    async changeValue(value, flag) {
      let val = await SurveyServices.getLastFiveResults(
        this.question.question_id
      )
      if (flag === 1) {
        this.replyOn = true
        this.addOn1 = false
        this.addOn2 = false
        this.questionData.comments = val.comments
      } else if (flag === 2) {
        this.replyOn = false
        this.addOn1 = true
        this.addOn2 = false
        this.questionData.comments = val.addOn1
      } else {
        this.replyOn = false
        this.addOn1 = false
        this.addOn2 = true
        this.questionData.comments = val.addon2
      }
      console.log(this.replyOn)
    },
    getData(answer) {
      this.resultObj.response_question_answer = answer
      this.resultObj.question_id = this.questionData.id
      this.sendResult()
    },
    sendResult() {
      this.$emit('updateQuestion', this.resultObj, this.number)
    },
    changeColor(color) {
      if (color) {
        this.color = ''
      } else {
        this.color = 'border:1px solid red'
      }
    },

    checkValidity() {
      if (this.questionData.required === true) {
        let flag = false
        for (
          let i = 0;
          i < this.resultObj.response_question_answer.length;
          i++
        ) {
          if (this.resultObj.response_question_answer[i].answerText != null) {
            flag = true
          }
        }
        if (flag === true) {
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
    },
  },
}
</script>

<style scoped>
.wordSelection {
  margin-bottom: 40px;
}

.wordSelection {
  margin-left: 14%;
}

.el-carousel__item p {
  white-space: normal;
  color: #475669;
  font-size: 10px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.question-box {
  border: 2px solid #eff2f5;
  border-radius: 4px;
  padding: 8px;
}

.action-btn {
  background-color: white;
  border: 1px solid black;
  padding: 5px 10px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  margin: 2px 10px 2px 130px;
  display: inline-block;
}

.last-btn {
  background-color: white;
  border: 1px solid black;
  padding: 5px 10px;
  color: black;
  font-size: 15px;
  border-radius: 5px;
  text-decoration: none;
  display: inline-block;
}

/*h1 {*/
/*  color: black;*/
/*  padding: 0 0 0 8px;*/
/*  font-family: Arial, Helvetica, sans-serif;*/
/*  font-style: normal;*/
/*  font-weight: bold;*/
/*  text-align: left;*/
/*  margin-right: 8px;*/
/*}*/

.title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  white-space: nowrap;
  /*font-family: Arial, Helvetica, sans-serif;*/
}

/*span {*/
/*  word-break: normal;*/
/*  width: auto;*/
/*  display: block;*/
/*  white-space: pre-wrap;*/
/*  word-wrap: break-word;*/
/*  overflow: hidden;*/
/*}*/
</style>
