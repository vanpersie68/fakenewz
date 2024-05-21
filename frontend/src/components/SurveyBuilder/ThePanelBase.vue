<template>
  <div class="panel-base">
    <div class="text-with-button">
      <h1>{{ editTitle }}</h1>
    </div>
    <line-base class="dark"></line-base>

    <!-- Edit Question Panel Content -->
    <div class="options" v-if="editingQuestion != null">
      <h2>{{ $t('panelBase.questionType') }}</h2>
      <dropdown-base :options="editorData.questionTypes" :currentType="editingQuestion.type"
        :icons="editorData.questionIcons" @input="handleQuestionType" />
      <line-base class="dark"></line-base>
      <div class="text-with-button">
        <h2>{{ $t('panelBase.answerReq') }}</h2>
        <toggle-base :toggled="editingQuestion.required" @handleToggle="toggleRequiredQuestion($store)"></toggle-base>
      </div>
      <line-base class="dark" v-if="editingQuestion != null"></line-base>

      <panel-options-articles v-if="editingQuestion.type === 'News post'" :question="editingQuestion" />

      <panel-options-text-entry v-if="editingQuestion.type === 'Text entry'" :question="editingQuestion" />

      <panel-options-button-row v-if="editingQuestion.type === 'Button row'" :question="editingQuestion" />

      <panel-options-multiple-choice v-if="editingQuestion.type === 'Multiple choice'" :question="editingQuestion" />

      <panel-options-number-scale v-if="editingQuestion.type === 'Number scale'" :question="editingQuestion" />

      <panel-options-drag-and-drop v-if="editingQuestion.type === 'Drag and Drop'" :question="editingQuestion" />
      <panel-options-rank-order v-if="editingQuestion.type === 'Rank order'" :question="editingQuestion" />
      <panel-options-matrix-table v-if="editingQuestion.type === 'Matrix table'" :question="editingQuestion" />
      <panel-options-sliders v-if="editingQuestion.type === 'Sliders'" :question="editingQuestion" />
      <panel-options-groups v-if="editingQuestion.type === 'Groups'" :question="editingQuestion" />
    </div>

    <!-- Edit Block Panel Content -->
    <panel-options-survey-flow v-else />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import DropdownBase from './DropdownBase.vue'
import LineBase from './LineBase.vue'
import PanelOptionsArticles from './PanelOptionsArticles.vue'
import PanelOptionsTextEntry from './PanelOptionsTextEntry.vue'
import PanelOptionsButtonRow from './PanelOptionsButtonRow.vue'
import ToggleBase from './ToggleBase.vue'

import store from '../../store/SurveyBuilder.js'
import PanelOptionsMultipleChoice from './PanelOptionsMultipleChoice.vue'
import PanelOptionsNumberScale from './PanelOptionsNumberScale.vue'
import PanelOptionsSurveyFlow from './PanelOptionsSurveyFlow.vue'
import PanelOptionsDragAndDrop from './PanelOptionsDragAndDrop.vue'
import PanelOptionsMatrixTable from './PanelOptionsMatrixTable.vue'
import PanelOptionsRankOrder from './PanelOptionsRankOrder.vue'
import PanelOptionsSliders from './PanelOptionsSliders.vue'
import PanelOptionsGroups from './PanelOptionsGroups.vue'

export default {
  name: 'ThePanelBase',
  store: store,
  components: {
    LineBase,
    ToggleBase,
    DropdownBase,
    PanelOptionsArticles,
    PanelOptionsTextEntry,
    PanelOptionsButtonRow,
    PanelOptionsMultipleChoice,
    PanelOptionsNumberScale,
    PanelOptionsSurveyFlow,
    PanelOptionsDragAndDrop,
    PanelOptionsMatrixTable,
    PanelOptionsRankOrder,
    PanelOptionsSliders,
    PanelOptionsGroups,
  },
  props: {
    editorData: {
      currentBlock: Number,
      blocks: Array,
    },
  },
  methods: {
    /**
     * Handle question type being changed from dropdown
     * @param data - is the data provided from the dropdown
     */
    handleQuestionType(data) {
      store.commit('handleQuestionType', {
        oldquestion: this.editingQuestion,
        type: data,
      })
    },
    /**
     * Toggle the question as being required
     * @param store - survey builder store
     */
    async toggleRequiredQuestion(store) {
      store.commit('toggle', {
        parent: this.editingQuestion,
        key: 'required',
      })

      await SurveyServices.patchQuestion(this.editingQuestion.id, {
        required: this.editingQuestion.required,
      })
    },
  },
  computed: {
    /**
     * Set the block to be edited
     * @returns block to be edited
     */
    editingBlock: function () {
      if (this.editorData.currentBlock == 0) {
        return null
      }

      let block = this.editorData.blocks.slice().filter((b) => {
        return b.order == this.editorData.currentBlock
      })

      // If currentBlock has not been set yet (on opening of this tab)
      if (this.editorData.currentBlock == null) {
        block = this.editorData.blocks.slice().filter((b) => {
          return b.order == 1
        })
      }

      return block[0]
    },
    /**
     * Set the question to be edited
     * @returns question to be edited
     */
    editingQuestion: function () {
      if (
        this.editingBlock == null ||
        this.editingBlock.questionData.currentQuestion == null
      ) {
        return null
      }

      let question = this.editingBlock.questionData.questions
        .slice()
        .filter((q) => {
          return q.order == this.editingBlock.questionData.currentQuestion
        })

      return question[0]
    },
    /**
     * Ensure if question or survey flow is being edited
     * @returns {string} question if question is being edited or survey flow if flow is being edited
     */
    editTitle: function () {
      if (this.editingQuestion != null) {
        return this.$t('panelBase.editQuestion')
      }
      return this.$t('panelBase.surveyFlow')
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
  direction: rtl;
}

.panel-base {
  margin-top: 0px;
  padding-top: 8px;
  min-height: calc(100vh - 56px);
  max-height: calc(100vh - 56px);
  display: flex;
  flex-basis: auto;
  align-items: flex-start;
  justify-content: flex-start;
  flex-direction: column;
  width: 500px;
  background-color: white;
  border-right: 1px solid #566370;

  position: sticky;
  left: 0;

  overflow: scroll;
}

.button-row {
  padding: 8px 8px 0px 8px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

h1,
h2 {
  color: black;
  padding: 0 16px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  text-align: left;
}

h1 {
  font-size: 24px;
}

h2 {
  font-size: 16px;
}

.options {
  width: 100%;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
}
</style>
