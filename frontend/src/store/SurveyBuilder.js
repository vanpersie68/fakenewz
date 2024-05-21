import Vue from 'vue'
import Vuex from 'vuex'
import i18n from '@/i18n.js'

// import VueI18n from 'vue-i18n'
import SurveyServices from '../services/SurveyServices'
import $ from 'jquery'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    mutex: false,
    survey: {},
    currentQuestionID: null,
    locksocket: null
  },
  mutations: {
    /**
     * Initialise survey based on response from backend
     * @param state - store state
     * @param response - response from backend
     */
    initSurvey(state, response) {
      Vue.set(state, 'survey', response)
    },
    setLockSocket(state, socket) {
      state.locksocket = socket;
    },
    SET_SURVEY(state, data) {
      state.survey = data;
    },
    /**
     * Set whether toggled or not toggled
     * @param state - store state
     * @param parent - where it is being toggled
     * @param key - what is being toggled
     */
    toggle(state, { parent, key }) {
      Vue.set(parent, key, !parent[key])
    },
    /**
     * toggle the title and the max/mid/min Title will become empty
     * @param state
     * @param parent
     * @param key
     * @param value
     */
    toggleTitle(state, { parent, key }) {
      Vue.set(parent, key, '')
    },
    /**
     * Update a value
     * @param state - store state
     * @param parent - where it is being updated
     * @param key - what is being updated
     * @param value - updated value
     */
    updateValue(state, { parent, key, value }) {
      Vue.set(parent, key, value)
    },
    /**
     * Remove the last element from a list
     * @param state - store state
     * @param list - list to remove from
     */
    removeLastElement(state, list) {
      list.pop()
    },
    /**
     * Insert an element at the end of an array
     * @param state - store state
     * @param list - list to add element to
     * @param element - element to be added
     */
    insertLastElement(state, { list, element }) {
      list.push(element)
    },
    /**
     * Update start of randomised section
     * @param state - store state
     * @param oldStart - old start point
     * @param newStart - new start point
     */
    updateStartWith(state, { oldStart, newStart }) {
      // Find index of section in randomSections
      let index = state.survey.editorData.randomSections.indexOf(
        state.survey.editorData.randomSections.filter(
          (e) => e.startWith == oldStart
        )[0]
      )

      // Update startWith to newStart
      state.survey.editorData.randomSections[index].startWith = newStart

      // Make sure display is in range
      let difference =
        state.survey.editorData.randomSections[index].endWith -
        state.survey.editorData.randomSections[index].startWith +
        1
      if (state.survey.editorData.randomSections[index].display > difference) {
        state.survey.editorData.randomSections[index].display = difference
      }
    },
    /**
     * Update end of randomised section
     * @param state - store state
     * @param oldStart - start point
     * @param newEnd - new end point
     */
    updateEndWith(state, { oldStart, newEnd }) {
      // Find index of section in randomSections
      let index = state.survey.editorData.randomSections.indexOf(
        state.survey.editorData.randomSections.filter(
          (e) => e.startWith == oldStart
        )[0]
      )

      // Update endWith to newEnd
      state.survey.editorData.randomSections[index].endWith = newEnd

      // Make sure display is in range
      let difference =
        state.survey.editorData.randomSections[index].endWith -
        state.survey.editorData.randomSections[index].startWith +
        1
      if (state.survey.editorData.randomSections[index].display > difference) {
        state.survey.editorData.randomSections[index].display = difference
      }
    },
    /**
     * Update button list by pushing or popping buttons
     * @param state - store state
     * @param question - button question to be updated
     * @param value - new length of button list
     */
    updateButtonList(state, { question, value }) {
      if (value > question.buttons.length) {
        for (let i = question.buttons.length; i < value; i++) {
          question.buttons.push({})
          Vue.set(question.buttons[i], 'text', i18n.t('app.buttonDefault'))
        }
      } else if (value < question.buttons.length) {
        for (let i = question.buttons.length; i > value; i--) {
          question.buttons.pop()
        }
      }
    },
    /**
     * swtich show condition
     * @param state
     * @param parent
     * @param key
     */
    reverseStatisticView(state, { parent, key }) {
      Vue.set(parent, key, !parent[key])
    },
    /**
     * Update social post addon list by pushing or popping buttons
     * @param state - store state
     * @param question - button question to be updated
     * @param value - new length of button list
     */
    updateAddonList(state, { question, value }) {
      if (value > question.addon.length) {
        for (let i = question.addon.length; i < value; i++) {
          question.addon.push({})
          Vue.set(question.addon[i], 'text', i18n.t('app.buttonDefault'))
        }
      } else if (value < question.addon.length) {
        for (let i = question.addon.length; i > value; i--) {
          question.addon.pop()
        }
      }
    },

    /**
     * Update multiple choice question choices list
     * @param state - store state
     * @param question - multiple choice question to be updated
     * @param value - new length of multiple choice question choices
     */
    updateMultiList(state, { question, value }) {
      if (value > question.choices.length) {
        for (let i = question.choices.length; i < value; i++) {
          question.choices.push({})
          Vue.set(question.choices[i], 'text', i18n.t('app.MCDefault'))
        }
      } else if (value < question.choices.length) {
        for (let i = question.choices.length; i > value; i--) {
          question.choices.pop()
        }
      }
    },
    /**
     * Handle tab being clicked
     * @param survey - current survey
     * @param tab - the tab clicked
     */
    handleTabClick({ survey }, tab) {
      survey.currentPage = tab
    },
    /**
     * Update the survey title
     * @param  survey - current survey
     * @param name - new survey title
     */
    updateSurveyTitle({ survey }, name) {
      Vue.set(survey, 'name', name)
      // console.log(survey.name)
    },
    /**
     * Update a block's title
     * @param state - store state
     * @param inner - inner
     * @param block - block in which title is changed
     */
    updateBlockTitle(state, { inner, block }) {
      Vue.set(block, 'title', inner)
    },
    /**
     * Update a block's description
     * @param state - store state
     * @param inner - inner
     * @param block - block in which description is changed
     */
    updateBlockDescription(state, { inner, block }) {
      Vue.set(block, 'description', inner)
    },
    /**
     * Set the inital block of a survey
     * @param survey - current survey
     */
    setInitialBlock({ survey }) {
      // If no block has been selected yet, automatically set the first one active
      survey.editorData.currentBlock = 1
    },
    /**
     * Handle block being clicked
     * @param survey - current survey
     * @param order - block index
     */

    //切换第几个表单
    handleBlockClick({ survey }, order) {
      // Set currentQuestion in previous block to null
      let prevBlock = survey.editorData.blocks.slice().filter((b) => {
        return b.order == survey.editorData.currentBlock
      })

      if (prevBlock[0] != null) {
        prevBlock[0].questionData.currentQuestion = null
      }

      // Set new currentBlock to order
      survey.editorData.currentBlock = order

      // Also set currentQuestion in this block to null
      let thisBlock = survey.editorData.blocks.slice().filter((b) => {
        return b.order == survey.editorData.currentBlock
      })

      if (thisBlock[0] != null) {
        thisBlock[0].questionData.currentQuestion = null
      }
    },
    /**
     * Handle question being clicked
     * @param survey - current survey
     * @param questionOrder - question index to be set
     * @param blockOrder - block index
     */

    //问题点击事件
    handleQuestionClick(state, { questionOrder, blockOrder }) {
      // Exit flowView
      state.survey.editorData.flowView = false
      // Set currentQuestion in previous block to null
      let prevBlock = state.survey.editorData.blocks.slice().filter((b) => {
        return b.order == state.survey.editorData.currentBlock
      })
      if (prevBlock[0] != null) {
        prevBlock[0].questionData.currentQuestion = null
      }
      // Set new question's enclosing block as currentBlock
      state.survey.editorData.currentBlock = blockOrder
      // Update currentQuestion in currentBlock to selected question
      let thisBlock = state.survey.editorData.blocks.slice().filter((b) => {
        return b.order == blockOrder
      })
      thisBlock[0].questionData.currentQuestion = questionOrder
      state.currentQuestionID = questionOrder
    },

    /**
     * Change block order (after drag and drop)
     * @param survey - current survey
     * @param newOrder - new index after dropping
     * @param block - block being moved
     */
    moveBlock({ survey }, { newOrder, block }) {
      console.log(newOrder, block.order)

      let oldOrder = block.order
      block.order = -1

      // Moving up
      if (newOrder < oldOrder) {
        for (let i = oldOrder - 1; i >= newOrder; i--) {
          console.log(i)
          survey.editorData.blocks.filter((e) => e.order == i)[0].order += 1
        }

        //
        // newOrder += 1

        // Moving down
      } else {
        for (let i = oldOrder + 1; i <= newOrder; i++) {
          survey.editorData.blocks.filter((e) => e.order == i)[0].order -= 1
        }
      }

      console.log('BLOCK', block, newOrder, block.order)

      block.order = newOrder

      console.log('BLOCK', block, newOrder, block.order)
    },
    /**
     * Insert a new block
     * @param state - store state
     * @param order - index of new block being inserted
     * @param block - block to be inserted
     */
    async insertNewBlock(state, { order, newBlock }) {
      if (state.mutex) {
        console.log('FAIL')
        return
      }

      // if (newBlock == null) {
      state.mutex = true
      // }

      // let isLockable = newBlock == null
      // console.log(isLockable)

      // If new insertion is not to the end of the survey
      if (order <= state.survey.editorData.blocks.length) {
        // Update order of all blocks following the new one, by descending order
        for (let i = state.survey.editorData.blocks.length; i >= order; i--) {
          let lastBlock = state.survey.editorData.blocks.filter((b) => {
            return b.order == i
          })

          await SurveyServices.patchBlock(lastBlock[0].id, {
            order: lastBlock[0].order + 1,
          })
          lastBlock[0].order++
        }
      }

      // Create the new block
      if (newBlock == null) {
        console.log('IS NULL!')
        newBlock = {
          order: order,
          survey: state.survey.id,
          title: i18n.t('app.newBlockTitle'),
        }
      }

      let response = await SurveyServices.postBlock(state.survey.id, {
        order: newBlock.order,
        survey: newBlock.survey,
        title: newBlock.title,
      })

      // append the questionData for the frontend, doesn't handle questions for duplicates yet
      response = {
        questionData: {
          currentQuestion: null,
          questions: [],
        },
        ...response,
        title: newBlock.title,
        description: newBlock.description,
      }

      // Insert a new block at order position 'order'
      state.survey.editorData.blocks.push(response)

      // Set currentQuestion of previous block to null
      let prevBlock = state.survey.editorData.blocks.slice().filter((b) => {
        return b.order == state.survey.editorData.currentBlock
      })

      if (prevBlock[0] != null) {
        prevBlock[0].questionData.currentQuestion = null
      }

      // Set as active block
      state.survey.editorData.currentBlock = order

      state.mutex = false

      console.log(state.mutex)
    },
    /**
     * Delete a block
     * @param state - store state
     * @param block - block to be deleted
     * @returns
     */
    async deleteBlock(state, block) {
      if (state.mutex) {
        console.log('FAIL')
        return
      }

      state.mutex = true

      await SurveyServices.deleteBlock(block.id)

      // Remove current block from list of blocks
      const index = state.survey.editorData.blocks.indexOf(block)
      let order = block.order

      // Decrement all random section bounds greater than order of removed
      for (let i = 0; i < state.survey.editorData.randomSections.length; i++) {
        if (state.survey.editorData.randomSections[i].startWith > order) {
          state.survey.editorData.randomSections[i].startWith--
        }

        if (state.survey.editorData.randomSections[i].endWith >= order) {
          state.survey.editorData.randomSections[i].endWith--
        }

        // Remove section if deleted block was only block in it
        if (
          state.survey.editorData.randomSections[i].endWith <
          state.survey.editorData.randomSections[i].startWith
        ) {
          state.survey.editorData.randomSections.splice(i, 1)
        }
      }

      state.survey.editorData.blocks.splice(index, 1)

      // Update order of all blocks following the new one, by descending order
      for (
        let i = order + 1;
        i <= state.survey.editorData.blocks.length + 1;
        i++
      ) {
        let lastBlock = state.survey.editorData.blocks.slice().filter((b) => {
          return b.order == i
        })

        await SurveyServices.patchBlock(lastBlock[0].id, {
          order: lastBlock[0].order - 1,
        })
        lastBlock[0].order--
      }

      // Set block after as active block
      if (order > state.survey.editorData.blocks.length) {
        order = state.survey.editorData.blocks.length
      }

      state.survey.editorData.currentBlock = order

      state.mutex = false

      console.log(state.mutex)
    },
    /**
     * Duplicate a question inside a block
     * @param state - store state
     * @param block - block in which question is located
     * @param question - question to be duplicated
     */
    async duplicateQuestion(state, { block, question }) {
      let sortedQuestions = block.questionData.questions
        .slice()
        .sort(function compare(a, b) {
          if (a.order < b.order) {
            return -1
          }
          return 1
        })

      let duplicate = JSON.parse(JSON.stringify(question))
      let order = duplicate.order + 1
      duplicate.order = order
      duplicate.title += ' copied version.'

      for (
        let i = block.questionData.questions.length - 1;
        i >= question.order;
        i--
      ) {
        sortedQuestions[i].order++
        await SurveyServices.patchQuestion(sortedQuestions[i].id, {
          order: sortedQuestions[i].order,
        })
      }

      const resp = await SurveyServices.duplicateQuestion(question.id, {
        order: duplicate.order,
      })
      duplicate.id = resp.id
      block.questionData.questions.push(duplicate)
    },
    /**
     * Delete a question inside a block
     * @param state - store state
     * @param block - block in which question is located
     * @param question - question to be deleted
     */
    async deleteQuestion(state, { block, question }) {
      await SurveyServices.deleteQuestion(question.id)

      // Remove current question from list of question
      const index = block.questionData.questions.indexOf(question)
      let order = question.order
      block.questionData.questions.splice(index, 1)

      // Update order of all questions following the new one, by descending order
      for (
        let i = order + 1;
        i <= block.questionData.questions.length + 1;
        i++
      ) {
        let lastBlock = block.questionData.questions.slice().filter((b) => {
          return b.order == i
        })

        await SurveyServices.patchQuestion(lastBlock[0].id, {
          order: lastBlock[0].order - 1,
        })
        lastBlock[0].order--
      }

      // Set question after as active question
      if (order > block.questionData.questions.length) {
        order = block.questionData.questions.length
      }

      block.currentQuestion = order
    },
    /**
     * Handle a change in type of answer for a text entry question
     * @param state - store state
     * @param question - text entry question with change of answer type
     * @param ansType - answer type to be changed to
     */
    handleTextAnswerType(state, { question, ansType }) {
      if (question.ansType != ansType) {
        switch (ansType) {
          case 'Text':
            Vue.set(question, 'type', 'Text entry')
            Vue.set(question, 'query', '')
            Vue.set(question, 'textBoxMax', 100)
            Vue.set(question, 'textBoxMin', 0)
            Vue.set(question, 'ansType', 'Text')
            break
          case 'Integer':
            Vue.set(question, 'type', 'Text entry')
            Vue.set(question, 'query', '')
            Vue.set(question, 'textBoxMax', 100)
            Vue.set(question, 'textBoxMin', 0)
            Vue.set(question, 'ansType', 'Integer')
            break
          case 'Decimal':
            Vue.set(question, 'type', 'Text entry')
            Vue.set(question, 'query', '')
            Vue.set(question, 'textBoxMax', 100)
            Vue.set(question, 'textBoxMin', 0)
            Vue.set(question, 'ansType', 'Decimal')
          case 'Date':
            Vue.set(question, 'type', 'Text entry')
            Vue.set(question, 'query', '')
            Vue.set(question, 'textBoxMax', 100)
            Vue.set(question, 'textBoxMin', 0)
            Vue.set(question, 'ansType', 'Date')
        }
      } else {
        return
      }
      question.ansType = ansType
    },
    /**
     * Handle change in question type
     * @param state - store state
     * @param question - question in which there is a change in type
     * @param type - new question type
     */
    async handleQuestionType(state, { oldquestion, type }) {
      console.log(state)
      console.log(state.survey.editorData.blocks[0].questionData)

      const order = oldquestion.order
      // const block_id = oldquestion.block
      const block_id =
        oldquestion.block ||
        state.survey.editorData.blocks.find((i) =>
          i.questionData.questions.find((j) => j.id === oldquestion.id)
        ).id

      let newQuestion = {
        type: type,
        name: oldquestion.title,
        required: false,
        order: order,
      }

      await SurveyServices.deleteQuestion(oldquestion.id)

      console.log(oldquestion, type, block_id, 'block_id')
      let response = await SurveyServices.postQuestion(block_id, newQuestion)
      let question = await SurveyServices.getQuestion(response.id)

      switch (type) {
        case 'News post':
          question.title = question.name
          delete question.name
          newQuestion = {
            ...question,
            ...question['type'],
            addon: [],
            type: type,
            articleStyle: 'Twitter',
            id: question.id,
          }
          break
        case 'Text entry':
          question.title = question.name
          newQuestion = {
            ...question,
            ...question['type'],
            type: type,
            id: question.id,
          }
          break
        case 'Number scale':
          question.title = question.name
          newQuestion = {
            ...question,
            ...question['type'],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
            },
          }
          console.log(newQuestion)
          break
        case 'Button row':
          question.title = question.name
          newQuestion = {
            ...question,
            ...question['type'],
            buttons: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
            },
            terminating: false,
          }
          break
        case 'Multiple choice':
          question.title = question.name
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
            },
          }

          break
      }

      let thisBlock = state.survey.editorData.blocks.filter(
        (e) => e.id == block_id
      )[0]
      thisBlock.questionData.questions.splice(
        thisBlock.questionData.questions.indexOf(oldquestion),
        1,
        newQuestion
      )
    },
    /**
     * Insert a new question into a block
     * @param state - store state
     * @param type - type of question
     * @param block - block in which question is being inserted
     */
    async insertNewQuestion(state, { type, block }) {
      let newQuestion = {
        type: type,
        name: i18n.t('app.newQuestionTitle'),
        required: false,
        order: block.questionData.questions.length + 1,
      }

      console.log(block.id, 'block.id')
      let response = await SurveyServices.postQuestion(block.id, newQuestion)
      let question = await SurveyServices.getQuestion(response.id)
      console.log('HERE IS THE QUESTION')
      console.log(question)
      console.log(question['type'])
      console.log(question['type'].numberMax)
      switch (type) {
        case 'News post':
          question.title = question.name
          delete question.name
          newQuestion = {
            ...question,
            ...question['type'],
            addon: [],
            type: type,
            typedata: question['type'],
            articleStyle: 'Twitter',
            id: question.id,
          }
          break
        case 'Text entry':
          newQuestion = {
            ...question,
            ...question['type'],
            type: type,
            typedata: question['type'],
            id: question.id,
          }
          break
        case 'Button row':
          newQuestion = {
            ...question,
            ...question['type'],
            buttons: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
            },
            terminating: false,
          }
          break
        case 'Multiple choice':
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
            },
          }
          console.log('1111111111111111111111111111')
          console.log(newQuestion)

          const rest1 = await SurveyServices.postMultiChoiceQuestion(
            newQuestion.typedata.id,
            {
              order: 1,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )

          const rest2 = await SurveyServices.postMultiChoiceQuestion(
            newQuestion.typedata.id,
            {
              order: 2,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )
          const rest3 = await SurveyServices.postMultiChoiceQuestion(
            newQuestion.typedata.id,
            {
              order: 3,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )
          console.log(rest1)
          Vue.set(newQuestion, 'choices', [
            {
              id: rest1.id,
              order: 1,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
            {
              id: rest2.id,
              order: 2,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
            {
              id: rest3.id,
              order: 3,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
          ])
          break
        case 'Matrix table':
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
              ...question['type'],
            },
          }
          console.log('1111111111111111111111111111')
          console.log(newQuestion)
          break
        case 'Sliders':
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
              ...question['type'],
            },
          }
          console.log('1111111111111111111111111111')
          console.log(newQuestion)
          break
        case 'Groups':
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
              ...question['type'],
            },
          }
          console.log('1111111111111111111111111111')
          console.log(newQuestion)
          break
        case 'Rank order':
          newQuestion = {
            ...question,
            ...question['type'],
            choices: [],
            type: type,
            id: question.id,
            typedata: {
              id: question['type'].id,
              // columnConfig: '[{}]'
            },
          }
          console.log('1111111111111111111111111111')
          console.log(newQuestion)

          const ro1 = await SurveyServices.postRankOrderQuestion(
            newQuestion.typedata.id,
            {
              order: 1,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )

          const ro2 = await SurveyServices.postRankOrderQuestion(
            newQuestion.typedata.id,
            {
              order: 2,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )
          const ro3 = await SurveyServices.postRankOrderQuestion(
            newQuestion.typedata.id,
            {
              order: 3,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            }
          )
          console.log(ro1)
          Vue.set(newQuestion, 'choices', [
            {
              id: ro1.id,
              order: 1,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
            {
              id: ro2.id,
              order: 2,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
            {
              id: ro3.id,
              order: 3,
              question: question.id,
              text: i18n.t('app.MCDefault'),
              title: i18n.t('app.MCDefault'),
            },
          ])
          break
        case 'Number scale':
          //question['type'].numberMax
          //question['type'].numberMin
          //question['type'].interval
          Vue.set(newQuestion, 'minNum', 0)
          Vue.set(newQuestion, 'maxNum', 0)
          Vue.set(newQuestion, 'interval', 1)
          Vue.set(newQuestion, 'minTitle', '')
          Vue.set(newQuestion, 'midTitle', '')
          Vue.set(newQuestion, 'maxTitle', '')
          Vue.set(newQuestion, 'minTitleOn', question['type'].minTitleOn)
          Vue.set(newQuestion, 'midTitleOn', question['type'].midTitleOn)
          Vue.set(newQuestion, 'maxTitleOn', question['type'].maxTitleOn)
          Vue.set(newQuestion, 'id', question.id)
          break
        // newQuestion = {
        //     ...question,
        //     ...question['type'],
        //     minNum: question['type'].numberMin,
        //     maxNum: question['type'].numberMax,
        //     interval: question['type'].interval,
        //     minTitle: question['type'].minTitle,
        //     midTitle: question['type'].middleTitle,
        //     maxTitle: question['type'].maxTitle,
        //     minTitleOn: true,
        //     midTitleOn: true,
        //     maxTitleOn: true,
        //     order: question.order,
        //     choices: [],
        //     type: type,
        //     id: question.id,
        //     typedata: {
        //         id: question['type'].id
        //     }
        // }
        //break;
        case 'Drag and Drop':
          Vue.set(newQuestion, 'choices', [
            {
              text: i18n.t('app.item'),
            },
          ])
          Vue.set(newQuestion, 'categories', [
            {
              text: i18n.t('app.category'),
            },
          ])
          break
        case 'Matrix':
          break
      }

      // Add new question to end of current block
      block.questionData.questions.push(newQuestion)

      // Set current question to new question
      block.questionData.currentQuestion = block.questionData.questions.length
    },
    incrementDisplay(state, start) {
      let thisSection = state.survey.editorData.randomSections.filter(
        (e) => e.startWith == start
      )[0]
      if (
        thisSection.display <
        thisSection.endWith - thisSection.startWith + 1
      ) {
        thisSection.display++
      }
      //Send the request to update the display value
    },
    decrementDisplay(state, start) {
      let thisSection = state.survey.editorData.randomSections.filter(
        (e) => e.startWith == start
      )[0]
      if (thisSection.display > 0) {
        thisSection.display--
      }
    },
    /**
     * Add a randomised section for blocks in flow editor
     * @param state - store state
     * @param order - index of block inside random section
     */
    addRandomSection(state, order) {
      state.survey.editorData.randomSections.push({
        startWith: order,
        endWith: order,
        display: 1,
      })
    },
    /**
     * Remove a randomised section in flow editor
     * @param state - store state
     * @param order - order of blocks inside randomised section
     */
    removeRandomSection(state, order) {
      let index = state.survey.editorData.randomSections.indexOf(
        state.survey.editorData.randomSections.filter(
          (section) => section.startWith == order
        )[0]
      )
      state.survey.editorData.randomSections.splice(index, 1)
    },
    /**
     * Handle dragging and dropping a question
     * @param survey - current survey
     * @param order - index of question
     * @param question - question being dragged and dropped
     * @param oldBlock - block from which question is being dragged
     */
    async insertQuestionDragDrop(survey, { order, block, question, oldBlock }) {
      let sortedQuestions = block.questionData.questions
        .slice()
        .sort(function compare(a, b) {
          if (a.order < b.order) {
            return -1
          }
          return 1
        })

      //change block and order data of question

      if (oldBlock === block) {
        if (question.order < order) {
          // update order of all questions in new block
          for (let i = order - 1; i > question.order - 1; i--) {
            sortedQuestions[i].order--
            await SurveyServices.patchQuestion(sortedQuestions[i].id, {
              order: sortedQuestions[i].order,
            })
          }

          question.order = order
          await SurveyServices.patchQuestion(question.id, {
            order: question.order,
          })
        } else if (question.order > order) {
          // update order of all questions in new block
          for (let i = question.order - 1; i >= order - 1; i--) {
            sortedQuestions[i].order++
            await SurveyServices.patchQuestion(sortedQuestions[i].id, {
              order: sortedQuestions[i].order,
            })
          }

          question.order = order
          await SurveyServices.patchQuestion(question.id, {
            order: question.order,
          })
        }
      } else {
        if (order == 0) {
          order++
        }

        question.order = order
        await SurveyServices.patchQuestion(question.id, {
          order: question.order,
          block: block.id,
        })

        // update order of all questions in new block
        for (
          let i = block.questionData.questions.length - 1;
          i >= question.order - 1;
          i--
        ) {
          sortedQuestions[i].order++
          await SurveyServices.patchQuestion(sortedQuestions[i].id, {
            order: sortedQuestions[i].order,
          })
        }
        block.questionData.questions.push(question)
      }
    },
    /**
     * Update order of questions after a question is removed from a block
     * @param survey - current survey
     * @param oldOrder - old order of question
     * @param question - question that was removed
     * @param newBlock - the new block question was moved to
     */
    async deleteQuestionDragDrop(
      survey,
      { oldOrder, oldBlock, question, newBlock }
    ) {
      let sortedQuestions = oldBlock.questionData.questions
        .slice()
        .sort(function compare(a, b) {
          if (a.order < b.order) {
            return -1
          }
          return 1
        })

      // Update delete order of all questions following the new one, by descending order
      for (let i = oldOrder; i < oldBlock.questionData.questions.length; i++) {
        sortedQuestions[i].order--
        await SurveyServices.patchQuestion(sortedQuestions[i].id, {
          order: sortedQuestions[i].order,
        })
      }

      const index = oldBlock.questionData.questions.indexOf(question)
      oldBlock.questionData.questions.splice(index, 1)
    },
    // addComment(state,res){
    //   console.log(res)

    // }
  },
  actions: {
    async addComment({ commit }, val) {
      // console.log(val)
      const res = await SurveyServices.postComment(val.questionId, {
        content: val.content,
      })
      // console.log(res)
      // commit('addComment', res)
    },
    updateSurvey({ commit }, data) {
      commit('SET_SURVEY', data);
    },
    setLockSocket({ commit }, socket) {
      commit('setLockSocket', socket);
    },
    /**
     * Load current survey
     */

    //获取数据的地方
    async loadSurvey({ commit }, surveyId) {
      const response = await SurveyServices.getSurveyData(surveyId)

      // Formats data type so that it works with the current Vue code
      response.currentPage = 'editor'

      if (response.blocks == null) {
        response.blocks = []
      }

      for (var i = 0; i < response.blocks.length; i++) {
        response.blocks[i] = {
          title: response.blocks[i].title,
          questionData: {
            currentQuestion: null,
            questions: response.blocks[i].questions,
          },
          ...response.blocks[i],
        }

        for (
          var k = 0;
          k < response.blocks[i].questionData.questions.length;
          k++
        ) {
          response.blocks[i].questionData.questions[k] = {
            ...response.blocks[i].questionData.questions[k].typedata,
            ...response.blocks[i].questionData.questions[k],
          }

          delete response.blocks[i].questionData.typedata
          response.blocks[i].questionData.questions[k].title =
            response.blocks[i].questionData.questions[k].name

          if (
            response.blocks[i].questionData.questions[k].type == 'Text entry'
          ) {
            response.blocks[i].questionData.questions[k].answerType = 'Text'
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Number entry'
          ) {
            response.blocks[i].questionData.questions[k].answerType = 'Integer'
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'News post'
          ) {
            response.blocks[i].questionData.questions[k].articleImage =
              response.blocks[i].questionData.questions[k].articleImageLink
            response.blocks[i].questionData.questions[k].likeCount =
              response.blocks[i].questionData.questions[k].articleLikes
            response.blocks[i].questionData.questions[k].shareCount =
              response.blocks[i].questionData.questions[k].articleShares
            response.blocks[i].questionData.questions[k].commentCount =
              response.blocks[i].questionData.questions[k].articleComments
            response.blocks[i].questionData.questions[k].retweetCount =
              response.blocks[i].questionData.questions[k].articleRetweets
            response.blocks[i].questionData.questions[k].sendCount =
              response.blocks[i].questionData.questions[k].articleSends
          }

          if (
            response.blocks[i].questionData.questions[k].type ==
            'Multiple choice'
          ) {
            for (
              var y = 0;
              y < response.blocks[i].questionData.questions[k].choices.length;
              y++
            ) {
              response.blocks[i].questionData.questions[k].choices[y].text =
                response.blocks[i].questionData.questions[k].choices[y].title
              response.blocks[i].questionData.questions[k].choices.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }
          if (
            response.blocks[i].questionData.questions[k].type == 'Rank order'
          ) {
            for (
              var y = 0;
              y < response.blocks[i].questionData.questions[k].choices.length;
              y++
            ) {
              response.blocks[i].questionData.questions[k].choices[y].text =
                response.blocks[i].questionData.questions[k].choices[y].title
              response.blocks[i].questionData.questions[k].choices.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Number scale'
          ) {
            console.log(response.blocks[i].questionData.questions[k])
            response.blocks[i].questionData.questions[k].minNum =
              response.blocks[i].questionData.questions[k].numberMin
            response.blocks[i].questionData.questions[k].maxNum =
              response.blocks[i].questionData.questions[k].numberMax
            response.blocks[i].questionData.questions[k].midTitle =
              response.blocks[i].questionData.questions[k].middleTitle
            response.blocks[i].questionData.questions[k].minTitleOn =
              response.blocks[i].questionData.questions[k].minTitleOn
            response.blocks[i].questionData.questions[k].maxTitleOn =
              response.blocks[i].questionData.questions[k].maxTitleOn
            response.blocks[i].questionData.questions[k].midTitleOn =
              response.blocks[i].questionData.questions[k].midTitleOn
            response.blocks[i].questionData.questions[k].interval =
              response.blocks[i].questionData.questions[k].interval

            if (response.blocks[i].questionData.questions[k].interval == 0) {
              response.blocks[i].questionData.questions[k].interval += 1
            }
          }

          if (
            response.blocks[i].questionData.questions[k].type == 'Button row'
          ) {
            // response.blocks[i].questionData.questions[k].goToEnd = false
            response.blocks[i].questionData.questions[k].terminating =
              response.blocks[i].questionData.questions[k].goToEnd
            for (
              var q = 0;
              q < response.blocks[i].questionData.questions[k].buttons.length;
              q++
            ) {
              response.blocks[i].questionData.questions[k].buttons[q].text =
                response.blocks[i].questionData.questions[k].buttons[
                  q
                ].buttonText
              // response.blocks[i].questionData.questions[k].buttons[q].goToEnd = false
              response.blocks[i].questionData.questions[k].buttons[
                q
              ].terminates =
                response.blocks[i].questionData.questions[k].buttons[q].goToEnd
              response.blocks[i].questionData.questions[k].buttons.sort(
                (a, b) => (a.order - b.order ? 1 : b.order - a.order ? -1 : 0)
              )
            }
          }
        }

        delete response.blocks[i].questions
      }

      response.title = response.name
      response.flowData = {}
      response.settingsData = {}

      response.editorData = {
        flowView: false,
        questionTypes: [
          'News post',
          'Multiple choice',
          'Text entry',
          'Number scale',
          'Button row',
          'Rank order',
          'Matrix table',
          'Sliders',
          'Groups',
          // "Matrix",
          // "Drag and Drop",
        ],
        questionIcons: [
          'fas fa-newspaper',
          'fas fa-dot-circle',
          'fas fa-pen',
          'fas fa-list-ol',
          'fas fa-grip-horizontal',
          "fas fa-th-list",
          "fa fa-table",
          "fa fa-sliders",
          "fa fa-columns",
        ],
        currentBlock: null,
        blocks: response.blocks,
        randomSections: response.randomSections,
      }
      delete response.blocks
      console.log(response, '整理数据的地方1')
      commit('initSurvey', response)
    },
    /**
     * Duplicate a specific block
     * @param state - store state
     * @param getters - getters
     * @param blockOrder - index of block being duplicated
     */
    async duplicateBlock({ state, getters }, blockOrder) {
      if (state.mutex) {
        console.log('FAIL')
        return
      }

      state.mutex = true

      let sortedBlocks = getters.sortedBlocks
      let duplicate = {}
      let thisBlock

      if (blockOrder != null) {
        thisBlock = getters.blocks.filter(
          (block) => block.order == blockOrder
        )[0]
        duplicate = JSON.parse(JSON.stringify(thisBlock))
      } else {
        duplicate = JSON.parse(JSON.stringify(getters.currentBlock))
        console.log('Current block order: ', duplicate.order)
      }

      // Increment all random section bounds greater than order of block being duplicated
      for (let i = 0; i < state.survey.editorData.randomSections.length; i++) {
        if (
          state.survey.editorData.randomSections[i].endWith >= duplicate.order
        ) {
          state.survey.editorData.randomSections[i].endWith++
        }

        if (
          state.survey.editorData.randomSections[i].startWith > duplicate.order
        ) {
          state.survey.editorData.randomSections[i].startWith++
        }
      }

      duplicate.order += 1
      console.log(sortedBlocks.length, duplicate.order)

      duplicate.title += ' copied version.'
      duplicate.questionData.currentQuestion = null

      for (let i = sortedBlocks.length - 1; i >= duplicate.order - 1; i--) {
        // console.log("sortedBlock: ", sortedBlocks[i].id)
        sortedBlocks[i].order++
        await SurveyServices.patchBlock(sortedBlocks[i].id, {
          order: sortedBlocks[i].order,
        })
      }

      console.log('starting')

      let currId
      if (blockOrder != null) {
        currId = thisBlock.id
      } else {
        currId = getters.currentBlock.id
      }

      const resp = await SurveyServices.duplicateBlock(currId, {
        order: duplicate.order,
      })

      console.log('finishing')
      duplicate.id = resp.id
      getters.blocks.push(duplicate)
      // state.survey.editorData.blocks.push(duplicate)

      state.mutex = false

      console.log(state.mutex)
    },
    /**
     * Clear contents of a block
     * @param getters - getters
     */
    async clearBlock({ getters }) {
      getters.currentBlock.questionData.questions.map(
        async (question) => await SurveyServices.deleteQuestion(question.id)
      )
      getters.currentBlock.questionData.questions = []
      getters.currentBlock.questionData.currentQuestion = null
    },
    /**
     * Fetch and set news article metadata
     * @param state - store state
     * @param resp - response from backend
     * @param resetValues - resetValues
     * @param question - news post question in which metadata is fetched
     */
    async fetchData(state, { resp, resetValues, question }) {
      Vue.set(question, 'articleURL', resp.url)
      Vue.set(question, 'articleImage', resp.image)
      Vue.set(question, 'articleSource', resp.urlShort)
      Vue.set(question, 'articleTitle', resp.title)
      Vue.set(question, 'articleSnippet', resp.description)
      resetValues()
    },
    /**
     * Fetch and set news article metadata
     * @param state - store state
     * @param resp - response from backend
     * @param question - news post question in which metadata is fetched
     */
    async fetchVideoData(state, { resp, question }) {
      Vue.set(question, 'articleURL', resp.embed_url)
      Vue.set(question, 'articleSource', resp.video_id)
      Vue.set(question, 'articleTitle', resp.video_title)
      Vue.set(question, 'articleUser', resp.articleUser)
      Vue.set(question, 'articleImageLink', resp.articleImageLink)
    },
  },
  getters: {
    wholeSurvey: (state) => state.survey,
    currentPage: (state) => state.survey.currentPage,
    surveyTitle: (state) => state.survey.name,
    questionTypes: (state) => state.survey.editorData.questionTypes,
    questionIcons: (state) => state.survey.editorData.questionIcons,
    editorData: (state) => state.survey.editorData,
    editingFlow: (state) => state.survey.flowData.editingFlow,
    flowView: (state) => state.survey.editorData.flowView,
    randomSections: (state) => {
      function compare(a, b) {
        if (a.startWith < b.startWith) {
          return -1
        }
        return 1
      }
      return state.survey.editorData.randomSections.slice().sort(compare)
    },
    blocks: (state) => {
      return state.survey.editorData.blocks
    },
    sortedBlocks: (state) => {
      function compare(a, b) {
        if (a.order < b.order) {
          return -1
        }
        return 1
      }

      return state.survey.editorData.blocks.slice().sort(compare)
    },
    sortedQuestions: (state) => (index) => {
      function compare(a, b) {
        if (a.order < b.order) {
          return -1
        }
        return 1
      }

      return state.survey.editorData.blocks[index].questionData.questions
        .slice()
        .sort(compare)
    },
    currentBlock: (state) => {
      let currentBlock = state.survey.editorData.blocks.slice().filter((b) => {
        return b.order == state.survey.editorData.currentBlock
      })
      return currentBlock[0]
    },


    //动态记录当前问题
    currentQuestion: (state) => {

      let currentBlock = state.survey.editorData.blocks.slice().filter((b) => {
        return b.order == state.survey.editorData.currentBlock
      })

      let currentQuestion = currentBlock[0].questionData.questions
        .slice()
        .filter((q) => {
          return q.order == currentBlock[0].questionData.currentQuestion
        })
      console.log('动态记录的问题currentQuestion[0]', currentQuestion[0]);
      return currentQuestion[0]
    },

    numBlocks: (state) => {
      return state.survey.editorData.blocks.length
    },
  },
})
