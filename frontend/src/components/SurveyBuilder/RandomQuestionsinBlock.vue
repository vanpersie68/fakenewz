<template>
  <div class="random" @click="$emit('randomClick', start)">
    <div class="block-header">
      <div class="block-title">
        <h1 v-if="title === 'Start'">
          {{ $t('randomElem.start') + showing }}
        </h1>
        <h1 v-else>
          {{ $t('randomElem.end') + showing }}
        </h1>
      </div>

      <!-- Buttons to the right of the heading -->
      <div class="button-row">
        <!-- <button-base
              class="primary square"
              :icon="'fas fa-grip-lines fa-lg'"
            /> -->
        <button-base
          v-if="title === 'Start'"
          class="purple square"
          :icon="'fas fa-minus fa-lg'"
          @buttonPress="$store.commit('decrementDisplay', start)"
        />
        <button-base
          v-if="title === 'Start'"
          class="purple square"
          :icon="'fas fa-plus fa-lg'"
          @buttonPress="$store.commit('incrementDisplay', start)"
        />

        <button-base
          v-if="title === 'Start'"
          class="purple square"
          :icon="'fas fa-trash fa-lg'"
          @buttonPress="$store.commit('removeRandomSection', start)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ButtonBase from '../../components/ButtonBase.vue'
import Vue from 'vue'
import store from '../../store/SurveyBuilder.js'

import { mapGetters } from 'vuex'

export default {
  components: { ButtonBase },
  name: 'RandomElement',
  store: store,
  props: {
    title: String,
    start: Number,
  },
  computed: {
    ...mapGetters(['randomSections']),
    showing() {
      let text = ''
      if (this.start != null) {
        let thisSection = this.randomSections.filter(
          (e) => e.startWith == this.start
        )[0]
        text = ` (show ${thisSection.display} out of ${
          thisSection.endWith - thisSection.startWith + 1
        })`
      }

      return text
    },
  },
  methods: {
    /**
     * Remove random element
     */
    removeElement(index) {
      store.commit('deleteBlock', this.sortedBlocks[index])
      this.showingQuestions.splice(index, 1)
      console.log(this.showingQuestions)
    },
    /**
     * Save whether questions of block are being toggled in random section
     */
    toggleQuestions(index) {
      Vue.set(this.showingQuestions, index, !this.showingQuestions[index])
    },
    /**
     * Sort questions inside a block
     * @returns Sorted questions in block
     */
    sortedQuestions(block) {
      function compare(a, b) {
        if (a.order < b.order) {
          return -1
        }
        return 1
      }
      return block.questionData.questions.slice().sort(compare)
    },
  },
}
</script>

<style scoped>
.random {
  max-width: 800px;
  min-width: 800px;
  margin: 8px auto;
  display: flex;
  flex-direction: column;
  background-color: #f5e4ff;
  /* padding: 8px; */
  border-radius: 8px;
  border-width: 2px;
  border-style: solid;
  border-color: white;
}

h1 {
  color: #9719e5;

  padding: 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  font-size: 24px;
  text-align: left;
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
  background-color: white;
}
</style>
