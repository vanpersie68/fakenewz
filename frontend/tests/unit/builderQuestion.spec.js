import { shallowMount } from '@vue/test-utils'
import BuilderQuestion from '../../src/components/SurveyBuilder/BuilderQuestion'
import store from '../../src/store/SurveyBuilder'
import SurveyServices from '../../src/services/SurveyServices'
import i18n from '@/i18n.js'

jest.mock('../../src/services/SurveyServices')

describe('Builder Question Tests', () => {
  beforeEach(async () => {
    //reset mock timers
    //jest.useRealTimers();

    // Create an empty survey in store, with a default block
    const survey = {
      editorData: {
        blocks: [],
      },
    }
    store.commit('initSurvey', survey)

    SurveyServices.postBlock.mockReturnValue({
      order: 1,
      id: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 1,
      id: 1,
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters.blocks[0],
    })
    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters.blocks[0],
    })
  })

  it('async undefined tests', async () => {
    //create shallow mount of BuilderQuestion
    console.log(store.getters['blocks'][0].questionData.questions)
    const wrapper = shallowMount(BuilderQuestion, {
      store,
      propsData: {
        block: store.getters['blocks'][0],
        blockOrder: 1,
        currentQuestion: 1,
        question: store.getters['blocks'][0].questionData.questions[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    const v1 = await wrapper.vm.updateQuestionTitle()

    expect(v1).toBe(undefined)
  })

  // it('pressQuestionOptions function test', () => {

  //     //create shallow mount of BuilderQuestion
  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     wrapper.vm.pressQuestionOptions()

  //     expect(wrapper.vm.$data.questionOptions).toBe(true)

  // })

  // it('isActiveQuestion function test', () => {

  //     //create shallow mount of BuilderQuestion
  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     console.log(wrapper.vm.isActiveQuestion)

  //     //check isActiveQuestion returns false
  //     expect(wrapper.vm.isActiveQuestion).toBe(true)

  //     // //change the boolean logic
  //     wrapper.vm.$props.question.order = 2

  //     //check it returns true now
  //     expect(wrapper.vm.isActiveQuestion).toBe(false)
  // })

  // it('updateQuestionTitle method test', () => {

  //     //create shallow mount of BuilderQuestion
  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     wrapper.vm.updateQuestionTitle({
  //         target: {
  //             innerHTML: "New Title"
  //         }
  //     });

  //     expect(store.getters['currentQuestion'].title.target.innerHTML).toEqual('New Title')

  // })

  // it('handleQuestionClick method test', () => {

  //     //create shallow mount of BuilderQuestion
  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     store.commit("insertNewBlock", {
  //         order: 2,
  //         newBlock: null
  //     })

  //     store.commit("insertNewQuestion", {
  //         type: "Text entry",
  //         block: store.getters.blocks[1]
  //     })

  //     wrapper.vm.handleQuestionClick()

  //     expect(store.getters['currentQuestion']).toEqual(wrapper.vm.$props.question)

  // })

  // it('getScaleList method test', () => {
  //     //create shallow mount of BuilderQuestion
  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     expect(wrapper.vm.getScaleList()).toEqual([])
  // })

  // it('unfocusQuestionOptions method test', () => {

  //     const wrapper = shallowMount(BuilderQuestion, {
  //         store,
  //         propsData: {
  //             block: store.getters['currentBlock'],
  //             blockOrder: 1,
  //             currentQuestion: 1,
  //             question: store.getters['currentQuestion'],
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     //jest.useFakeTimers();

  //     wrapper.vm.unfocusQuestionOptions()

  //     //expect(setTimeout).toHaveBeenCalledTimes(1)

  //     expect(wrapper.vm.$data.questionOptions).toBe(false)

  // })
})
