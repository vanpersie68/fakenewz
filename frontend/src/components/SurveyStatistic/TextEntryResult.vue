<template>
  <div class="question-box">
    <div>
      <div class="word">
        <h1 class="questionNumber" v-model="index">
          Q{{ index + 1 }} {{ questions.type }}
        </h1>
        <h2 class="questionName" v-model="questions.title">
          {{ questions.title }}
        </h2>
        <p class="questionCount" v-model="questions">
          {{ questions.answered }} out of {{ questions.count }} people answered
          this question
        </p>
      </div>
      <div class="wordSelection">
        <el-carousel
          style="width: 400px"
          height="200px"
          :interval="5000"
          arrow="always"
        >
          <el-carousel-item
            v-for="item in this.questions.answers"
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
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

export default {
  props: {
    question: Object,
    index: Number,
  },
  data() {
    return {
      questions: {},
    }
  },
  methods: {
    async randomSelection() {
      this.questions.answers = await SurveyServices.getRandomFiveResults(
        this.question.question_id
      )
      //     [
      //   "While Secrets Of Dumbledore looks very nice, it’s a drudge to watch.",
      //   "The Secrets of Dumbledore actually has me looking forward to the next movie.",
      //   "It's a lot better than the second and it justifies having 'Fantastic Beasts'",
      //   "Hello World",
      //   "To further expand the debugging capabilities, advanced JSON",
      // ]
    },
    async lastSelection() {
      this.questions.answers = await SurveyServices.getLastFiveResults(
        this.question.question_id
      )
    },
  },
  created() {
    this.number = this.index
    this.questions = this.question
    console.log('Text Entry Answer', this.questions.answers)
    // this.questions.answers = this.question.answers;
  },
  name: 'TextEntryResult',
}
</script>
<style>
.word h2 {
  font-weight: bold;
}

.word {
  margin-left: 10%;
}

.wordSelection {
  margin-bottom: 40px;
}

.wordSelection {
  margin-left: 15%;
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
  width: 550px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px;
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
</style>
