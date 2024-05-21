<template>
  <div class="block-class">
    <div class="title">
      <h1>{{ blockData.title }}</h1>
    </div>
    <p style="white-space: pre-line" class="block_description">
      {{ blockData.description }}
    </p>
    <div class="questionBlock">
      <div
        v-for="(item, index) in randomQuestions"
        :key="randomQuestions.id"
        class="question"
      >
        <RankOrder
          v-if="item.type === 'Rank order'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <MatrixTable
          v-if="item.type === 'Matrix table'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <Sliders
          v-if="item.type === 'Sliders'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <Groups
          v-if="item.type === 'Groups'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <MultipleChoice
          v-if="item.type === 'Multiple choice'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <TextEntry
          v-if="item.type === 'Text entry'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <NumberScale
          v-if="item.type === 'Number scale'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <NewsPost
          v-if="item.type === 'News post'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          :ref="'block' + blockIndex + 'question' + index"
        />
        <ButtonRow
          v-if="item.type === 'Button row'"
          :question="item"
          :index="index"
          @updateQuestion="updateQuestion"
          @updateJumpBlockId="updateJumpBlockId"
          :ref="'block' + blockIndex + 'question' + index"
        />
      </div>
    </div>
  </div>
</template>
<script>
import MultipleChoice from '@/components/SurveyTaker/MultipleChoice'
import TextEntry from '@/components/SurveyTaker/TextEntry'
import NumberScale from '@/components/SurveyTaker/NumberScale'
import ButtonRow from '@/components/SurveyTaker/ButtonRaw'
import NewsPost from '@/components/SurveyTaker/NewsPost'
import RankOrder from '@/components/SurveyTaker/RankOrder'
import MatrixTable from '@/components/SurveyTaker/MatrixTable'
import Sliders from '@/components/SurveyTaker/Sliders'
import Groups from '@/components/SurveyTaker/Groups'

export default {
  name: 'Block',
  components: {
    ButtonRow,
    NumberScale,
    TextEntry,
    MultipleChoice,
    NewsPost,
    RankOrder,
    MatrixTable,
    Sliders,
    Groups,
  },
  props: {
    block: Object,
    index: Number,
    currentId: Number,
    uuid: String,
  },
  data() {
    return {
      createTime: '',
      endTime: '',
      blockData: {},
      answerData: {
        // "uuid": "",
        block_id: 0,
        response_questions: [],
      },
      blockIndex: 0,
      jumpBlockId: 0,
      randomQuestions: [],
    }
  },
  methods: {
    updateQuestion(data, index) {
      // console.log('updateQuestion ', data)
      this.answerData.response_questions[index] = data

      for (
        let i = 0;
        i <
        this.answerData.response_questions[index].response_question_answer
          .length;
        i++
      ) {
        this.answerData.response_questions[index].response_question_answer[
          i
        ].uuid = this.answerData.uuid + index + i
      }
      this.endTime = new Date()
      // console.log(this.endTime)
      if (this.currentId !== this.block.id) {
        this.createTime = null
        this.endTime = null
      }
      this.answerData.createTime = this.createTime
      this.answerData.endTime = this.endTime

      this.$emit('updateBlock', this.answerData, this.blockIndex)
    },
    updateJumpBlockId(id) {
      this.jumpBlockId = id
      this.$emit('updateJumpBlockId', this.jumpBlockId)
    },
    checkValidity() {
      let validity = true
      for (let i = 0; i < this.blockData.questionData.questions.length; i++) {
        if (
          !this.$refs[
            'block' + this.blockIndex + 'question' + i
          ][0].checkValidity()
        ) {
          validity = false
        }
      }
      return validity
    },
  },
  watch: {
    currentId: function (currentId) {
      if (this.currentId === this.block.id) {
        this.createTime = new Date()
        this.answerData.createTime = this.createTime
      }
    },
  },
  created() {
    if (this.currentId === this.block.id) {
      this.createTime = new Date()
      this.answerData.createTime = this.createTime
    }
    this.blockData = this.block
    this.blockIndex = this.index
    this.answerData = {
      uuid: this.uuid + this.index,
      block_id: this.blockData.id,
      response_questions: [],
    }
    this.randomQuestions = this.blockData.questionData.questions.map(
      (question, index) => {
        return {
          ...question,
          originalOrder: index + 1,
        }
      }
    )
    this.randomQuestions.sort(() => Math.random() - 0.5)
    // console.log('RANDOM QUESTIONS: ', this.randomQuestions)
  },
  mounted() {
    // console.log('CHILD SEND EMIT')
    this.$emit('updateBlock', this.answerData, this.blockIndex)
    this.$emit('randomQuestions', this.randomQuestions)
  },
}
</script>

<style scoped>
.title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  white-space: nowrap;
  font-family: Arial, Helvetica, sans-serif;
}
.block_description {
  padding-left: 10px;
  word-wrap: break-word;
}

@media (min-width: 1130px) {
  .block-class {
    border: 2px solid #eff2f5;
    border-radius: 4px;
    margin: 8px;
    padding: 30px;
    background: #f7f7f7;
  }
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    text-align: left;
    margin-right: 8px;
    table-layout: fixed;
    white-space: normal;
    word-wrap: break-word;
  }
  .question {
    margin-bottom: 30px;
  }
}

@media (max-width: 1129px) and (min-width: 890px) {
  .block-class {
    border: 2px solid #eff2f5;
    border-radius: 4px;
    margin: 8px;
    padding: 30px;
    background: #f7f7f7;
  }
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    text-align: left;
    margin-right: 8px;
    word-break: break-all;
    white-space: normal;
    word-wrap: break-word;
  }
  .question {
    margin-bottom: 25px;
  }
}

@media (max-width: 889px) {
  .block-class {
    border: 2px solid #eff2f5;
    border-radius: 4px;
    margin: 0px;
    padding: 0px;
    background: #f7f7f7;
  }
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-size: 24px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    text-align: left;
    margin-right: 8px;
    word-break: break-all;
    white-space: normal;
    word-wrap: break-word;
  }
  .question {
    margin-bottom: 15px;
  }
}
</style>
