<template>
  <div class='block' :class="isActiveBlock ? 'active' : ''" @mouseup='handleBlockClick' @mousedown='handleFocus'>
    <div class='block-header'>
      <div class='block-title'>
        <input type='text' v-model='block.title' @blur='updateBlockTitle' class='h1-tb' :style="$i18n.locale === 'ur' ? 'text-align: right;' : 'text-align: left;'
          " />
      </div>
      <div class='opt-container'>
        <div class='popup' :class="blockOptions
            ? currentBlock.order == numBlocks &&
              block.questionData.questions.length < 1
              ? 'show above'
              : 'show below'
            : ''
          " :style="$i18n.locale === 'ur' ? 'left: 0px;' : 'right: 0px;'">
          <h3>{{ $t('builderBlock.blockOptions') }}</h3>
          <line-base class='dark' />
          <li>
            <button-base class='secondary min' :icon="'fas fa-clone fa-me'"
                           :title="$t('builderBlock.blockQuestionRandom')"
                           @mousedown="$store.dispatch('duplicateBlock')" />
          </li>

          <line-base class='dark' />
          <li>
            <button-base class='secondary min red' :icon="'fas fa-eraser fa-me'"
                          :title="$t('builderBlock.clearBlock')"
                          @mousedown="$store.dispatch('clearBlock')" />
          </li>

          <li>
            <button-base class='secondary min red' :icon="'fas fa-trash fa-me'"
                          :title="$t('builderBlock.deleteBlock')"
                          @mousedown="$store.commit('deleteBlock', block)" />
          </li>
          
        </div>
        <button-base class='secondary square' :icon="'fas fa-ellipsis-h fa-lg'" @buttonPress='pressBlockOptions'
                     @buttonUnfocus='unfocusBlockOptions' />
      </div>
    </div>
    <line-base class='light'></line-base>
    <h3>{{ $t('builderBlock.descriptionText') }}</h3>
    <text-area :placeholder="$t('builderBlock.typeDescription')" :block='block' @handleInput='updateBlockdescription' />
    <Container :get-child-payload='getChildPayload' group-name='1' @drop='onDrop'>
      <line-base class='light'></line-base>
      <Draggable v-for='question in sortedQuestions' :key='question.order' :question='question'>
        <builder-question :key='question.order' :blockOrder='block.order'
                          :currentQuestion='block.questionData.currentQuestion' :question='question' :block='block' />
      </Draggable>
    </Container>
    <div class='container'>
      <div class='popup' :class="newQuestion ? 'show above' : ''">
        <h3>{{ $t('builderBlock.questionType') }}</h3>
        <line-base class='dark' />
        <ul v-for='type in questionTypes' :key='type'>
          <li>
            <button-base class='secondary min' :title="$t('builderBlock.' + type.toString().replace(/\s/g, ''))"
                         @mousedown='insertNewQuestion(type)' />
          </li>
        </ul>
      </div>
      <button-base class='primary standard popup-btn' :icon="'fas fa-plus fa-me'"
                   :title="$t('builderBlock.addNewQuestion')" @buttonPress='pressNewQuestion'
                   @buttonUnfocus='unfocusNewQuestion' />
    </div>
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'
import { Container, Draggable } from 'vue-smooth-dnd'
import { applyDrag } from '../../services/DragDropHelpers.js'

import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import BuilderQuestion from './BuilderQuestion.vue'
import TextBox from './TextBox.vue'

import store from '../../store/SurveyBuilder.js'
import { mapGetters } from 'vuex'
import TextArea from './TextArea.vue'

export default {
  name: 'BuilderBlock',
  store: store,
  components: {
    ButtonBase,
    LineBase,
    BuilderQuestion,
    TextArea,
    TextBox,
    Container,
    Draggable,
  },
  props: {
    block: Object,
  },
  data: function () {
    return {
      newQuestion: false,
      blockOptions: false,
    }
  },
  computed: {
    ...mapGetters(['numBlocks', 'currentBlock', 'questionTypes']),
    /**
     * Sort questions inside a block
     * @returns Sorted questions in block
     */
    sortedQuestions: function() {
      function compare(a, b) {
        if (a.order < b.order) {
          return -1
        }
        return 1
      }
      return this.block.questionData.questions.slice().sort(compare)
    },
    /**
     * Check if block is active
     * @returns true if active and false otherwise
     */

    isActiveBlock: function() {
      if (
        this.currentBlock != null &&
        this.currentBlock.order == this.block.order
      ) {
        console.log();
        return true
      }

      if (this.currentBlock == null && this.block.order == 1) {
        // Notify store that currentBlock.order should be 1
        store.commit('setInitialBlock')
        return true
      }

      return false
    },
    /**
     * Check if a block has an active question
     * @returns true if so and false otherwise
     */
    hasActiveQuestion: function () {
      if (this.block.questionData.currentQuestion != null) {
        return true
      }
      return false
    },
  },
  methods: {
    /**
     * Update and save block title
     */
    async updateBlockTitle(e) {
      await SurveyServices.patchBlock(this.block.id, {
        title: this.block.title
      })
    },
    async handleFocus () {
      store.state.locksocket.send(this.block.id)
    },
    /**
     * Update and save block description
     */
    async updateBlockdescription(e) {
      store.commit('updateBlockDescription', {
        inner: e,
        block: this.block
      })
      console.log('执行了更新描述');
      await SurveyServices.patchBlock(this.block.id, { description: e })
    },
    /**
     * Handle block being clicked
     * @param e - event
     */
    handleBlockClick(e) {
      // If path contains element with classname 'question', don't select block
      // The handleQuestionClick function will do this automatically
      let pathObj = e.path || (e.composedPath && e.composedPath())

      let path = pathObj.map((element) => element.className)
      if (path.includes('question') || path.includes('question active')) {
        return
      }

      store.commit('handleBlockClick', this.block.order)
      console.log('点击之后是否会存起来',this.block.order);
      
    },
    /**
     * Display popup for block options
     */
    pressBlockOptions() {
      this.blockOptions = !this.blockOptions
    },
    /**
     * Hide popup for block options
     */
    unfocusBlockOptions() {
      this.blockOptions = false
    },
    /**
     * Show dropdown when new question button is pressed
     */
    pressNewQuestion() {
      this.newQuestion = !this.newQuestion
    },
    /**
     * Hide dropdown when new question button unpressed
     */
    unfocusNewQuestion() {
      this.newQuestion = false
    },
    /**
     * Insert a new question based on dropdown for question type
     * @param type - type of question
     */
    insertNewQuestion(type) {
      store.commit('insertNewQuestion', { type: type, block: this.block })
      this.newQuestion = false
    },
    /**
     * Handle dropping a block after dragging
     */
    onDrop(dropResult) {
      applyDrag(this.block, dropResult)
    },
    /**
     * Get payload object to be passed to onDrop
     */
    getChildPayload(index) {
      return this.sortedQuestions[index - 1]
    },
  },
}
</script>

<style scoped lang= 'scss'>
@import '../../assets/textbox.css';

html:lang(ur) * {
  text-align: right;
  direction: rtl;
}

@media only screen and (max-width: 767px) {
  .block {
    width: 100%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    background-color: white;
    padding: 8px;
    border-radius: 8px;
    border-width: 2px;
    border-style: solid;
    border-color: white;
  }
}

@media only screen and (min-width: 768px) {
  .block {
    max-width: 800px;
    min-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    background-color: white;
    padding: 8px;
    border-radius: 8px;
    border-width: 2px;
    border-style: solid;
    border-color: white;
  }
}

.active,
.block.active:hover {
  border-color: #1947e5;
}

.block:hover {
  border-color: #566370;
}

h1 {
  color: black;
  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  font-size: 24px;
  text-align: left;
}

h3 {
  color: black;
  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  text-align: left;
  font-size: 16px;
}

.block-title:hover > *[contenteditable='true'],
.block-title:focus > *[contenteditable='true'] {
  /* background-color: #eff2f5;
  outline: 0; */
  border: 2px solid #566370;
}

.block-title > *[contenteditable='true'] {
  padding: 8px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
}

.block-title {
  width: 100%;
  margin-right: 8px;
}

.block-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding-left: 8px;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.container {
  position: relative;
  display: flex;
  justify-content: center;
  margin: 0 auto;
}

.opt-container {
  position: relative;
  display: flex;
  justify-content: right;
}

.popup {
  position: absolute;

  z-index: 2;
  display: none;

  width: 300px;
  margin: 0 auto;
  border: 2px solid #566370;
  border-radius: 8px;
  padding: 0 8px;
  background-color: #eff2f5;
}

.below {
  top: 62px;
}

.above {
  bottom: 62px;
}

.show {
  display: block;
}

.popup ul,
.popup ul li {
  list-style-type: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.popup ul li button {
  width: 100%;
  margin: 8px auto;
}

@media (max-width: 889px) {
  .block {
    width: 300px;
  }
}

@media only screen and (min-width: 889px) {
  .block {
    max-width: 800px;
    min-width: 800px;

  }

}
</style>
