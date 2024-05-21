<template>
  <div class="flow-container">
    <Container
      style="width: 820px"
      @drop="onDrop"
      :get-child-payload="getChildPayload"
      :group-name="'blocks'"
    >
      <Draggable
        v-for="(block, index) in orderedFlow"
        :key="index"
        class="element-container"
      >
        <random-element
          v-if="block.start"
          :title="'Start'"
          :start="orderedFlow[index].startInd"
        />

        <random-element v-else-if="block.start != null" :title="'End'" />
        <div v-else class="block">
          <div class="block-header">
            <div class="block-title" style="width: 550px">
              <h1 style="width: 100%; overflow-wrap: break-word">
                {{
                  `${$t('flowEditor.block')} ${orderedFlow[index].order}: ${
                    orderedFlow[index].title
                  } (${orderedFlow[index].questionData.questions.length}Q${
                    orderedFlow[index].questionData.questions.length == 1
                      ? ''
                      : 's'
                  })`
                }}
              </h1>
            </div>

            <!-- Buttons to the right of the heading -->
            <div class="button-row">
              <button-base
                v-if="!orderedFlow[index].inRandom"
                class="purple square"
                :icon="'fas fa-random fa-lg'"
                @buttonPress="
                  addRandomSection(
                    orderedFlow[index].order,
                    orderedFlow[index].survey
                  )
                "
                :hover="'Random'"
              />
              <button-base
                class="primary square"
                :icon="
                  showingQuestions[orderedFlow[index].order - 1]
                    ? 'fas fa-eye-slash fa-lg'
                    : 'fas fa-eye fa-lg'
                "
                :hover="'Info'"
                @buttonPress="toggleQuestions(orderedFlow[index].order - 1)"
              />
              <button-base
                class="primary square"
                :icon="'fas fa-clone fa-lg'"
                :hover="'Duplicate'"
                @buttonPress="duplicateElement(orderedFlow[index].order - 1)"
              />

              <button-base
                class="destructive square"
                :icon="'fas fa-trash fa-lg'"
                @buttonPress="removeElement(orderedFlow[index].order - 1)"
                :hover="'Delete'"
              />
            </div>
          </div>

          <line-base
            v-if="showingQuestions[orderedFlow[index].order - 1]"
            class="light"
          ></line-base>

          <h3
            v-if="
              showingQuestions[orderedFlow[index].order - 1] &&
              sortedBlocks[orderedFlow[index].order - 1].questionData.questions
                .length == 0
            "
          >
            {{ $t('flowEditor.noQuestions') }}
          </h3>

          <div
            v-else-if="showingQuestions[orderedFlow[index].order - 1]"
            class="questions"
          >
            <div
              v-for="question in sortedQuestions(orderedFlow[index])"
              :key="question.order"
              class="question-block"
            >
              <div class="question-lead">
                <i
                  class="fa-lg"
                  :class="questionIcons[questionTypes.indexOf(question.type)]"
                ></i>
                <h3>
                  {{ `${question.type}` }}
                </h3>
              </div>
              <h2>
                {{
                  `Q${question.order}${question.required ? '*' : ''}: ${
                    question.title
                  }`
                }}
              </h2>
            </div>
          </div>
        </div>
      </Draggable>
    </Container>

    <line-base class="light" />
  </div>
</template>

<script>
import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import Vue from 'vue'
import store from '../../store/SurveyBuilder.js'
import SurveyServices from '@/services/SurveyServices'

import { mapGetters } from 'vuex'
import RandomElement from './RandomElement.vue'
import { Container, Draggable } from 'vue-smooth-dnd'
import { applyFlowDrag } from '../../services/DragDropHelpers.js'

export default {
  components: { ButtonBase, LineBase, RandomElement, Container, Draggable },
  name: 'TheFlowEditor',
  store: store,
  computed: {
    ...mapGetters([
      'sortedBlocks',
      'questionTypes',
      'questionIcons',
      'randomSections',
    ]),
    /**
     * Handle random section flow logic
     */
    orderedFlow() {
      let flow = JSON.parse(JSON.stringify(this.sortedBlocks))

      // Add random elements to flow
      for (let i = 0; i < this.randomSections.length; i++) {
        // If randomised section is empty, remove
        if (
          this.randomSections[i].startWith > this.sortedBlocks.length ||
          this.randomSections[i].endWith > this.sortedBlocks.length
        ) {
          store.commit('removeRandomSection', this.randomSections[i].startWith)
          break
        }

        // Find index of first element, then insert a start signal before it
        let startInd = flow.indexOf(
          flow.filter((e) => e.order == this.randomSections[i].startWith)[0]
        )
        flow.splice(startInd, 0, {
          start: true,
          startInd: this.randomSections[i].startWith,
        })

        // Find index of last element, then insert a end signal after it
        let endInd =
          flow.indexOf(
            flow.filter((e) => e.order == this.randomSections[i].endWith)[0]
          ) + 1
        flow.splice(endInd, 0, {
          start: false,
          startInd: this.randomSections[i].startWith,
        })
      }
      let j = 0
      while (flow[j].id == null) {
        j++
      }
      console.log(flow[j].id)
      var surveyId = flow[j].survey
      var res = []
      for (let i = 0; i < this.randomSections.length; i++) {
        var randoms = {
          survey: surveyId,
          display: this.randomSections[i].display,
          startWith: this.randomSections[i].startWith,
          endWith: this.randomSections[i].endWith,
          index: i,
        }
        console.log('this.randomSections[', i, ']', this.randomSections[i])
        res[i] = randoms
      }
      console.log('res[i]', res)
      SurveyServices.patchRandomSections(surveyId, JSON.stringify(res))

      // Add randomised flag to blocks between random starts and ends
      let inRandom = false
      for (let i = 0; i < flow.length; i++) {
        if (flow[i].start == null) {
          Vue.set(flow[i], 'inRandom', inRandom)
        } else if (flow[i].start) {
          inRandom = true
        } else {
          inRandom = false
        }
      }
      for (let i = 0; i < flow.length; i++) {
        if (flow[i].order == null) {
          continue
        }
        SurveyServices.patchUpdateOrder(flow[i].id, { order: flow[i].order })
      }
      console.log('FLOW', flow)
      return flow
    },
  },
  data() {
    return {
      // Array of false for every block
      showingQuestions: [...Array(store.getters.numBlocks)].map(
        (_, e) => false
      ),
    }
  },
  methods: {
    /**
     * Remove a block from flow editor and survey
     */
    removeElement(index) {
      if (
        confirm(
          'Deleting this block will delete it permanently from your survey builder. Are you sure you want to delete this block?'
        )
      ) {
        store.commit('deleteBlock', this.sortedBlocks[index])
        this.showingQuestions.splice(index, 1)
      }
    },
    /**
     * Duplicate a block in flow editor and survey
     */
    duplicateElement(index) {
      store.dispatch('duplicateBlock', this.sortedBlocks[index].order)
      this.showingQuestions.splice(index + 1, 0, false)
    },
    /**
     * Toggle whether to show questions in a block or not
     */
    toggleQuestions(index) {
      Vue.set(this.showingQuestions, index, !this.showingQuestions[index])
    },
    /**
     * Sort the questions in a block to be shown
     */
    sortedQuestions(block) {
      console.log('BLOCK', block)

      function compare(a, b) {
        if (a.order < b.order) {
          return -1
        }
        return 1
      }

      return block.questionData.questions.slice().sort(compare)
    },
    /**
     * Add a random section to a block
     */
    addRandomSection(order, survey) {
      store.commit('addRandomSection', order)
      console.log('ID ID', survey)
      // SurveyServices.postRandomSections(survey, order, {
      //   order: this.order,
      //   survey_id: this.survey,
      // });
    },
    /**
     * Handle dropping a block after dragging
     */
    onDrop(dropResult) {
      applyFlowDrag(this.orderedFlow, dropResult)

      // Modify showingQuestions array to match new drop
      let thisShowing =
        this.showingQuestions[
          this.orderedFlow[dropResult.removedIndex].order - 1
        ]
      this.showingQuestions.splice(
        this.orderedFlow[dropResult.removedIndex].order - 1,
        1
      )

      // If moving down
      if (dropResult.addedIndex > dropResult.removedIndex) {
        this.showingQuestions.splice(
          this.orderedFlow[dropResult.addedIndex].order - 1,
          0,
          thisShowing
        )
      } else {
        this.showingQuestions.splice(
          this.orderedFlow[dropResult.addedIndex].order - 1,
          0,
          thisShowing
        )
      }
    },
    /**
     * Get payload object to be passed to onDrop
     */
    getChildPayload(index) {
      return this.orderedFlow[index]
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
  direction: rtl;
}

.flow-container {
  background-color: #eff2f5;
  width: 100%;
  min-height: calc(100vh - 56px - 56px);
  overflow: scroll;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  align-items: center;
  margin: 0;
}

.element-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.block {
  max-width: 800px;
  min-width: 800px;
  margin: 8px auto;
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 8px;
  border-radius: 8px;
  border-width: 2px;
  border-style: solid;
  border-color: white;
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

h2 {
  color: #566370;
  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  font-size: 21px;
  text-align: left;
}

h3 {
  color: #566370;
  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  /* text-align: left; */
  font-size: 16px;
}

.block-title {
  display: flex;
  align-items: center;
  width: 100%;
  /* gap: 8px; */
}

.block-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding-left: 8px;
  gap: 16px;
}

.button-row {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-end;
}

.questions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.question-block {
  display: flex;
  /* padding: 16px; */
  gap: 16px;
  border: 2px solid #eff2f5;
  border-radius: 8px;
  align-items: center;
}

.question-lead {
  /* background-color: red; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 18px 16px 0 16px;
  padding-right: 16px;
  border-right: 2px solid #eff2f5;
  text-align: center;
  min-width: 100px;
  max-width: 100px;
  /* flex-wrap: nowrap; */
}

.question-lead i {
  color: #566370;
}

.options {
  display: flex;
  justify-content: flex-start;
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
</style>
