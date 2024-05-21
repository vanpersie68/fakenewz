<template>
  <div class="mainBlock">
    <h1 class="block_description">{{ blockData.title }}</h1>
    <div
      v-for="(item, index) in blockData.questions"
      :key="blockData.questions.id"
    >
      <MultipleChoiceResult
        v-if="item.type === 'Multiple choice'"
        :question="item"
        :index="index"
      />
      <MatrixTableResult
        v-if="item.type === 'Matrix table'"
        :question="item"
        :index="index"
      />
      <GroupsResult
        v-if="item.type === 'Groups'"
        :question="item"
        :index="index"
      />
      <TextEntryResult
        v-if="item.type === 'Text entry'"
        :question="item"
        :index="index"
      />
      <NumberScaleResult
        v-if="item.type === 'Number scale'"
        :question="item"
        :index="index"
      />
      <ButtonRowResult
        v-if="item.type === 'Button row'"
        :question="item"
        :index="index"
      />
      <NewsPostResult
        v-if="item.type === 'News post'"
        :question="item"
        :index="index"
      />
    </div>
  </div>
</template>

<script>
import TextEntryResult from './TextEntryResult'
import NumberScaleResult from './NumberScaleResult'
import MultipleChoiceResult from './MultipleChoiceResult'
import ButtonRowResult from './ButtonRowResult'
import NewsPostResult from './NewsPostResult'
import MatrixTableResult from './MatrixTableResult'
import GroupsResult from './GroupsResult'
export default {
  methods: {},
  props: {
    block: Object,
    index: Number,
  },
  data() {
    return {
      blockData: {},
      blockIndex: 0,
    }
  },
  method: {
    updateQuestion(data, index) {
      this.answerData.response_questions[index] = data
      console.log(this.answerData.response_questions)
      this.endTime = new Date()
      if (this.currentId !== this.block.id) {
        this.createTime = ''
        this.endTime = ''
      }
      this.answerData.createTime = this.createTime
      this.answerData.endTime = this.endTime
      this.$emit('updateBlock', this.answerData, this.blockIndex)
    },
  },
  created() {
    this.blockData = this.block
    this.blockIndex = this.index
  },
  name: 'Results',
  components: {
    NewsPostResult,
    ButtonRowResult,
    MultipleChoiceResult,
    NumberScaleResult,
    TextEntryResult,
    MatrixTableResult,
    GroupsResult,
  },
}
</script>
<style>
.block_description {
  margin-left: 20px;
}

.mainBlock {
  width: 610px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px 20px 20px 35%;
  padding: 8px;
}
</style>
