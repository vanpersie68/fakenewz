import { shallowMount } from '@vue/test-utils'
import TextArea from '../../src/components/SurveyBuilder/TextArea.vue'
import store from '../../src/store/SurveyBuilder'

describe('TextArea component test suite', () => {
  beforeEach(() => {
    // Create an empty survey in store, with a default block
    const survey = {
      editorData: {
        blocks: [],
      },
    }
    store.commit('initSurvey', survey)
  })

  it('submitInput method test without blocks', () => {
    const wrapper = shallowMount(TextArea, {
      propsData: {
        placeholder: 'Fake name',
        block: store.getters['currentBlock'],
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.submitInput()

    //test that the right object is returned and it is empty
    expect(wrapper.emitted().handleInput[0]).toEqual([''])
  })

  it('submitInput method test with existing block', () => {
    store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters.blocks[0],
    })

    const wrapper = shallowMount(TextArea, {
      propsData: {
        placeholder: 'Fake name',
        block: store.getters['currentBlock'],
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.submitInput()

    //test that the right object is returned and it is undefined
    expect(wrapper.emitted().handleInput[0]).toEqual([undefined])
  })
})
