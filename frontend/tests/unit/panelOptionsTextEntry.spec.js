import { shallowMount } from '@vue/test-utils'
import PanelOptionsTextEntry from '../../src/components/SurveyBuilder/PanelOptionsTextEntry'
import store from '../../src/store/SurveyBuilder'

describe('Panel Options Text Entry test', () => {
  beforeEach(() => {
    // Create an empty survey in store, with a default block
    const survey = {
      editorData: {
        blocks: [],
      },
    }
    store.commit('initSurvey', survey)

    store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters.blocks[0],
    })
  })

  it('check component exists test', () => {
    // Create a shallow mount of the PanelOptionsTextEntry vue file
    const wrapper = shallowMount(PanelOptionsTextEntry, {
      propsData: {
        question: {},
      },
      mocks: {
        $t: () => {},
      },
    })

    expect(wrapper.vm.$props.question).toEqual({})
  })

  it('handleTextAnswerType function test ', () => {
    // Create a shallow mount of the PanelOptionsTextEntry vue file
    const wrapper = shallowMount(PanelOptionsTextEntry, {
      propsData: {
        question: store.getters['currentQuestion'],
      },
      mocks: {
        $t: () => {},
      },
    })

    // Call the handleTextAnswerType function
    wrapper.vm.handleTextAnswerType({
      options: ['Text', 'Integer', 'Decimal'],
      index: 0,
    })

    //console.log(wrapper.emitted())

    // Test parameter is updated
    expect(store.getters['currentQuestion'].answerType).toEqual('Text')
  })
})
