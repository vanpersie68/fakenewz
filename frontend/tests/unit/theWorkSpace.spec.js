import { shallowMount } from '@vue/test-utils'
import TheWorkSpace from '../../src/components/SurveyBuilder/TheWorkSpace.vue'
import store from '../../src/store/SurveyBuilder'
import SurveyServices from '../../src/services/SurveyServices'

jest.mock('../../src/services/SurveyServices')

describe('The Work Space test', () => {
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

  // it('sortedBlocks computed test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             title: "Test Block",
  //             editorData: {
  //                 currentBlock: 2,
  //                 blocks: [{
  //                     order: 2,
  //                     title: "Block 2"
  //                 }, {
  //                     order: 1,
  //                     title: "Block 1"
  //                 }, {
  //                     order: 4,
  //                     title: "Block 4"
  //                 }, {
  //                     order: 3,
  //                     title: "Block 3"
  //                 }],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Test that the blocks are sorted
  //     expect(wrapper.vm.sortedBlocks).toEqual([{
  //         order: 1,
  //         title: "Block 1"
  //     }, {
  //         order: 2,
  //         title: "Block 2"
  //     }, {
  //         order: 3,
  //         title: "Block 3"
  //     }, {
  //         order: 4,
  //         title: "Block 4"
  //     }, ]);

  // })

  // it('handleBlockClick function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             title: "Test Block",
  //             editorData: {
  //                 currentBlock: 2,
  //                 blocks: [{
  //                     order: 2,
  //                     title: "Block 2"
  //                 }, {
  //                     order: 1,
  //                     title: "Block 1"
  //                 }, {
  //                     order: 4,
  //                     title: "Block 4"
  //                 }, {
  //                     order: 3,
  //                     title: "Block 3"
  //                 }],
  //             },
  //         },
  //     })

  //     // Call the handleSelection function to move to current page
  //     wrapper.vm.handleBlockClick(0);

  //     console.log(wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(wrapper.emitted().handleBlockClick[0]).toEqual([0]);

  // })

  // it('handleQuestionClick function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the handleQuestionClick function
  //     wrapper.vm.handleQuestionClick({
  //         questionOrder: 1,
  //         blockOrder: 2
  //     });

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().handleQuestionClick[0]).toEqual([{
  //         questionOrder: 1,
  //         blockOrder: 2
  //     }]);

  // })

  // it('setInitialBlock function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the setInitialBlock function
  //     wrapper.vm.setInitialBlock();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().setInitialBlock[0]).toEqual([]);

  // })

  it('handleTitleInput function test', async () => {
    // Create a shallow mount of the TheWorkSpace vue file
    const wrapper = shallowMount(TheWorkSpace, {
      // propsData: {
      //     editorData: {
      //         blocks: [],
      //     },
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

    // Call the handleTitleInput function
    wrapper.vm.handleTitleInput({
      target: {
        innerHTML: 'New Title',
      },
    })

    // Test parameter is emitted
    expect(store.getters['surveyTitle']).toEqual('New Title')
  })

  // it('handleBlockTitleInput function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the handleBlockTitleInput function
  //     wrapper.vm.handleBlockTitleInput({
  //         inner: 1,
  //         blockOrder: 2
  //     });

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().handleBlockTitleInput[0]).toEqual([{
  //         inner: 1,
  //         blockOrder: 2
  //     }]);

  // })

  // it('insertNewQuestion function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the insertNewQuestion function
  //     wrapper.vm.insertNewQuestion("New type");

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().insertNewQuestion[0]).toEqual(["New type"]);

  // })

  // it('insertNewBlock function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the insertNewBlock function
  //     wrapper.vm.insertNewBlock(3);

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().insertNewBlock[0]).toEqual([3]);

  // })

  // it('fetchData function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     const mock_data = jest.fn();

  //     // Call the fetchData function
  //     wrapper.vm.fetchData({
  //         url: "URL",
  //         resetValues: mock_data
  //     });

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().fetchData[0]).toEqual([{
  //         url: "URL",
  //         resetValues: mock_data
  //     }]);

  // })

  // it('refreshImage function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the refreshImage function
  //     wrapper.vm.refreshImage("New URL");

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().refreshImage[0]).toEqual(["New URL"]);

  // })

  // it('updateLikes function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateLikes function
  //     wrapper.vm.updateLikes(100);

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateLikes[0]).toEqual([100]);

  // })

  // it('updateComments function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateComments function
  //     wrapper.vm.updateComments(100);

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateComments[0]).toEqual([100]);

  // })

  // it('updateShares function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateShares function
  //     wrapper.vm.updateShares(100);

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateShares[0]).toEqual([100]);

  // })

  // it('duplicateBlock function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the duplicateBlock function
  //     wrapper.vm.duplicateBlock();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().duplicateBlock[0]).toEqual([]);

  // })

  // it('clearBlock function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the clearBlock function
  //     wrapper.vm.clearBlock();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().clearBlock[0]).toEqual([]);

  // })

  // it('deleteBlock function test', () => {
  //     // Create a shallow mount of the TheWorkSpace vue file
  //     const wrapper = shallowMount(TheWorkSpace, {
  //         propsData: {
  //             editorData: {
  //                 blocks: [],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the deleteBlock function
  //     wrapper.vm.deleteBlock();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().deleteBlock[0]).toEqual([]);

  // })
})
