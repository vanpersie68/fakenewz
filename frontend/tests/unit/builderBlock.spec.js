import { shallowMount } from '@vue/test-utils'
import store from '../../src/store/SurveyBuilder'
import BuilderBlock from '../../src/components/SurveyBuilder/BuilderBlock'
import SurveyServices from '../../src/services/SurveyServices'
import i18n from '@/i18n.js'

jest.mock('../../src/services/SurveyServices')

describe('Builder Block Tests', () => {
  beforeEach(async () => {
    //reset mock timers
    jest.useRealTimers()

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

  it('check if the block has a current question', async () => {
    // Create shallow mount of BuilderBlock
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    expect(wrapper.vm.hasActiveQuestion).toBe(false)

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    expect(wrapper.vm.hasActiveQuestion).toBe(true)
  })

  it('retrieve a sorted list of questions in the block', () => {
    // Create shallow mount of BuilderBlock
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: {
          questionData: {
            questions: [
              { order: 2, id: 7 },
              { order: 3, id: 1 },
              { order: 1, id: 5 },
            ],
          },
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    expect(wrapper.vm.sortedQuestions).toEqual([
      { order: 1, id: 5 },
      { order: 2, id: 7 },
      { order: 3, id: 1 },
    ])
  })

  it('updateBlockTitle method test', async () => {
    // Create shallow mount of BuilderBlock
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.patchBlock.mockReturnValue(true)

    const variable = await wrapper.vm.updateBlockTitle({
      target: {
        innerHTML: 'New Title',
      },
    })

    expect(variable).toEqual(undefined)
  })

  it('handleBlockClick method test', () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    // store.commit("insertNewBlock", {
    //     order: 2,
    //     newBlock: null
    // })

    wrapper.vm.handleBlockClick({
      path: ['fake'],
    })

    expect(store.getters['currentBlock'].order).toBe(1)
  })

  it('handleBlockClick question option method test', async () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.postBlock.mockReturnValue({
      order: 2,
      id: 2,
    })

    await store.commit('insertNewBlock', {
      order: 2,
      newBlock: null,
    })

    wrapper.vm.handleBlockClick({
      path: [
        {
          className: 'question',
        },
      ],
    })

    expect(store.getters['currentBlock'].order).toBe(2)

    // wrapper.vm.handleBlockClick({
    //     path: ['fake']
    // });

    // expect(store.getters['currentBlock'].order).toBe(1)
  })

  it('pressBlockOptions method test', () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.pressBlockOptions()

    expect(wrapper.vm.$data.blockOptions).toBe(true)

    wrapper.vm.pressBlockOptions()

    expect(wrapper.vm.$data.blockOptions).toBe(false)
  })

  it('pressNewQuestion method test', () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.pressNewQuestion()

    expect(wrapper.vm.$data.newQuestion).toBe(true)

    wrapper.vm.pressNewQuestion()

    expect(wrapper.vm.$data.newQuestion).toBe(false)
  })

  // it('insertNewQuestion method test', () => {
  //     const wrapper = shallowMount(BuilderBlock, {
  //         propsData: {
  //             block: store.getters.blocks[0]
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     SurveyServices.getQuestion.mockReturnValue({
  //         type: "Text entry",
  //         name: i18n.t('app.newQuestionTitle'),
  //         required: false,
  //         order: 2,
  //         id: 2,
  //     })

  //     wrapper.vm.insertNewQuestion('Text entry')

  //     store.commit("handleQuestionClick", {
  //         questionOrder: 2,
  //         blockOrder: 1
  //     })

  //     expect(store.getters['currentQuestion'].type).toEqual('Text entry')

  //     // wrapper.vm.pressNewQuestion()

  //     // expect(wrapper.vm.$data.blockOptions).toBe(false)

  // })

  it('unfocusBlockOptions method test', () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    //jest.useFakeTimers();

    wrapper.vm.unfocusBlockOptions()

    //expect(setTimeout).toHaveBeenCalledTimes(1)

    expect(wrapper.vm.$data.blockOptions).toBe(false)
  })

  it('unfocusNewQuestion method test', () => {
    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    //jest.useFakeTimers();

    wrapper.vm.unfocusNewQuestion()

    //expect(setTimeout).toHaveBeenCalledTimes(1)

    expect(wrapper.vm.$data.newQuestion).toBe(false)
  })

  it('isActiveBlock computed test', () => {
    // // Create an empty survey in store, with a default block
    // const survey = {
    //     editorData: {
    //         blocks: []
    //     }
    // }
    // store.commit("initSurvey", survey)

    const wrapper = shallowMount(BuilderBlock, {
      propsData: {
        block: store.getters.blocks[0],
      },
      mocks: {
        $t: () => {},
      },
    })

    expect(wrapper.vm.isActiveBlock).toBe(true)
  })
})
