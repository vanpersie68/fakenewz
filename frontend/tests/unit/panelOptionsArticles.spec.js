import { shallowMount } from '@vue/test-utils'
import PanelOptionsArticles from '../../src/components/SurveyBuilder/PanelOptionsArticles'
import store from '../../src/store/SurveyBuilder'

const { survey } = store

describe('Panel Options Articles test', () => {
  // Create a shallow mount of the PanelOptionsArticles vue file
  const wrapper = shallowMount(PanelOptionsArticles, {
    store: survey,
    propsData: {
      question: {},
    },
    mocks: {
      $t: () => {},
    },
  })

  // it('handleLikesToggle function test ', () => {

  //     // Call the handleLikesToggle function
  //     wrapper.vm.handleLikesToggle();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().handleLikesToggle[0]).toEqual([]);

  // })

  // it('handleCommentsToggle function test ', () => {

  //     // Call the handleCommentsToggle function
  //     wrapper.vm.handleCommentsToggle();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().handleCommentsToggle[0]).toEqual([]);

  // })

  // it('handleSharesToggle function test ', () => {

  //     // Call the handleSharesToggle function
  //     wrapper.vm.handleSharesToggle();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().handleSharesToggle[0]).toEqual([]);

  // })

  it('handlePostStyle function test ', () => {
    const data = {
      options: ['New Style'],
      index: 0,
    }
    // Call the handlePostStyle function
    wrapper.vm.handlePostStyle(data)

    console.log(survey)

    // Test parameter is emitted
    //expect(wrapper.emitted().handlePostStyle[0]).toEqual(["New Style"]);
  })
})
