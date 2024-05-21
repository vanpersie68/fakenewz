import { shallowMount } from '@vue/test-utils'
import store from '../../src/store/SurveyBuilder'
import theToolBar from '../../src/components/SurveyBuilder/theToolBar.vue'
import SurveyServices from '../../src/services/SurveyServices'

jest.mock('../../src/services/SurveyServices')

describe('Tool Bar test', () => {
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

  it('handleTabClick same page function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'editor'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    // Test that the currentPage defaults to editor
    expect(store.getters['currentPage']).toEqual('editor')

    // Call the handleSelection function to move to current page
    wrapper.vm.handleTabClick('editor')

    // Test that the currentPage defaults to editor
    expect(store.getters['currentPage']).toEqual('editor')

    // console.log(wrapper.emitted())

    // // Test that the selected option is emitted
    // expect(wrapper.emitted()).toEqual({});
  })

  it('handleTabClick to flow function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'flow'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    // Call the handleSelection function to move to flow
    wrapper.vm.handleTabClick('flow')

    // Test that the selected option is emitted
    expect(store.getters['currentPage']).toEqual('flow')
  })

  it('handleTabClick to settings function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'flow'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    // Call the handleSelection function to move to flow
    wrapper.vm.handleTabClick('settings')

    // Test that the selected option is emitted
    expect(store.getters['currentPage']).toEqual('settings')
  })

  it('handleTabClick to preview function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'flow'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    // Call the handleSelection function to move to flow
    wrapper.vm.handleTabClick('preview')

    // Test that the selected option is emitted
    expect(store.getters['currentPage']).toEqual('preview')
  })

  it('handleTabClick default fallback function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'flow'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    // Call the handleSelection function to move to flow
    wrapper.vm.handleTabClick('random string')

    // Test that the selected option is emitted
    expect(store.getters['currentPage']).toEqual('editor')
  })

  it('handleTabClick default fallback 2 function test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(theToolBar, {
      // propsData: {
      //     currentPage: 'flow'
      // },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    //store.commit("handleTabClick", "preview")
    wrapper.vm.handleTabClick('editor')
    expect(store.getters['currentPage']).toEqual('editor')
    wrapper.vm.handleTabClick('flow')
    expect(store.getters['currentPage']).toEqual('flow')
    wrapper.vm.handleTabClick('settings')
    expect(store.getters['currentPage']).toEqual('settings')
    wrapper.vm.handleTabClick('preview')
    expect(store.getters['currentPage']).toEqual('preview')

    // Call the handleSelection function to move to flow
    wrapper.vm.handleTabClick('random string')

    // Test that the selected option is emitted
    expect(wrapper.vm.currentPage).toEqual('editor')
  })
})
