import { shallowMount } from '@vue/test-utils'
import store from '../../src/store/SurveyBuilder'
import PostTwitterEditable from '../../src/components/SurveyBuilder/PostTwitterEditable'
import SurveyServices from '../../src/services/SurveyServices'

jest.mock('../../src/services/SurveyServices')

describe('Post Twitter Editable test', () => {
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

  it('isImage null computed test', () => {
    // Create a shallow mount of the PostTwitterEditable vue file
    const wrapper = shallowMount(PostTwitterEditable, {
      propsData: {
        question: store.getters.currentQuestion,
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that isImage is false when this.image is null
    expect(wrapper.vm.isImage).toBe(false)
  })

  // it('isImage empty string computed test', () => {
  //     // Create a shallow mount of the PostTwitterEditable vue file
  //     const wrapper = shallowMount(PostTwitterEditable, {
  //         propsData: {
  //             question: store.getters.currentQuestion
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Test that isImage is false when this.image is null
  //     expect(wrapper.vm.isImage).toBe(false);

  // })

  it('isImage normal string computed & updateTitle method test', async () => {
    // Create a shallow mount of the PostTwitterEditable vue file
    const wrapper = shallowMount(PostTwitterEditable, {
      propsData: {
        question: store.getters.currentQuestion,
      },
      mocks: {
        $t: () => {},
      },
    })

    const mock_fn = jest.fn()
    // mock_fn.mockReturnValue(true)
    SurveyServices.getLinkInformation.mockReturnValue({
      url: 'test-url',
      image: 'test-image',
      urlShort: 'test-urlShort',
      title: 'test-title',
      description: 'test-description',
    })

    await store.dispatch('fetchData', {
      url: 'test.com',
      resetValues: mock_fn,
      question: store.getters.currentQuestion,
    })

    expect(store.getters.currentQuestion.articleImage).toEqual('test-image')
    //console.log(store.getters.currentQuestion)

    wrapper.vm.updateTitle({
      target: {
        innerHTML: 'New Title',
      },
    })

    // Test that isImage is false when this.image is null
    expect(wrapper.vm.isImage).toBe(true)
  })

  it('updateSource method test', async () => {
    // Create a shallow mount of the PostTwitterEditable vue file
    const wrapper = shallowMount(PostTwitterEditable, {
      propsData: {
        question: store.getters.currentQuestion,
      },
      mocks: {
        $t: () => {},
      },
    })

    const mock_fn = jest.fn()
    // mock_fn.mockReturnValue(true)
    SurveyServices.getLinkInformation.mockReturnValue({
      url: 'test-url',
      image: 'test-image',
      urlShort: 'test-urlShort',
      title: 'test-title',
      description: 'test-description',
    })

    await store.dispatch('fetchData', {
      url: 'test.com',
      resetValues: mock_fn,
      question: store.getters.currentQuestion,
    })

    expect(store.getters.currentQuestion.articleImage).toEqual('test-image')
    //console.log(store.getters.currentQuestion)

    wrapper.vm.updateSource({
      target: {
        innerHTML: 'New Title',
      },
    })

    // Test that isImage is false when this.image is null
    expect(store.getters.currentQuestion.articleSource).toBe('New Title')
  })

  it('updateSnippet method test', async () => {
    // Create a shallow mount of the PostTwitterEditable vue file
    const wrapper = shallowMount(PostTwitterEditable, {
      propsData: {
        question: store.getters.currentQuestion,
      },
      mocks: {
        $t: () => {},
      },
    })

    const mock_fn = jest.fn()
    // mock_fn.mockReturnValue(true)
    SurveyServices.getLinkInformation.mockReturnValue({
      url: 'test-url',
      image: 'test-image',
      urlShort: 'test-urlShort',
      title: 'test-title',
      description: 'test-description',
    })

    await store.dispatch('fetchData', {
      url: 'test.com',
      resetValues: mock_fn,
      question: store.getters.currentQuestion,
    })

    expect(store.getters.currentQuestion.articleImage).toEqual('test-image')
    //console.log(store.getters.currentQuestion)

    wrapper.vm.updateSnippet({
      target: {
        innerHTML: 'New Title',
      },
    })

    // Test that isImage is false when this.image is null
    expect(store.getters.currentQuestion.articleSnippet).toBe('New Title')
  })
})
