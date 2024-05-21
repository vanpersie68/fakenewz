import { shallowMount } from '@vue/test-utils'
import ThePanelBase from '../../src/components/SurveyBuilder/ThePanelBase.vue'
import store from '../../src/store/SurveyBuilder'

describe('The Panel Base test', () => {
  // it('editTitle editing question computed test', () => {
  //     // Create a shallow mount of the ThePanelPase vue file
  //     const wrapper = shallowMount(ThePanelBase, {
  //         propsData: {
  //             editorData: {
  //                 currentBlock: 1,
  //                 blocks: [{
  //                     order: 1,
  //                     title: "Block 1",
  //                     questionData: {
  //                         currentQuestion: 1,
  //                         questions: [{
  //                             type: "multi-choice",
  //                             title: "Default Question Title 4",
  //                             required: true,
  //                             order: 1,
  //                         }, ]
  //                     },
  //                 }, ],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Test that the editTitle is Question when editingQuestion != null
  //     expect(wrapper.vm.editTitle).toEqual("Question");

  // })

  // it('editTitle editing block computed test', () => {
  //     // Create a shallow mount of the ThePanelPase vue file
  //     const wrapper = shallowMount(ThePanelBase, {
  //         propsData: {
  //             editorData: {
  //                 currentBlock: 1,
  //                 blocks: [{
  //                     order: 1,
  //                     title: "Block 1",
  //                     questionData: {
  //                         currentQuestion: null,
  //                         questions: [{
  //                             type: "multi-choice",
  //                             title: "Default Question Title 4",
  //                             required: true,
  //                             order: 1,
  //                         }, ]
  //                     },
  //                 }, ],
  //             },
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Test that the editTitle is Block when editingQuestion == null && editingBlock != null
  //     expect(wrapper.vm.editTitle).toEqual("Block");

  // })

  it('editTitle editing nothing computed test', () => {
    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: 0,
          blocks: [],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that the editTitle is '' when editingQuestion == null && editingBlock != null
    expect(wrapper.vm.editTitle).toEqual('')
  })

  it('editingBlock currentBlock valid computed test', () => {
    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: 2,
          blocks: [
            {
              order: 1,
              title: 'Block 1',
              questionData: {
                currentQuestion: null,
                questions: [
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 4',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
            {
              order: 2,
              title: 'Block 2',
              questionData: {
                currentQuestion: null,
                questions: [
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 5',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
          ],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that the second block is editingBlock (as given)
    expect(wrapper.vm.editingBlock).toEqual(
      wrapper.vm.$props.editorData.blocks[1]
    )
  })

  it('editingBlock currentBlock null computed test', () => {
    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: null,
          blocks: [
            {
              order: 1,
              title: 'Block 1',
              questionData: {
                currentQuestion: null,
                questions: [
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 4',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
          ],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that the first block is editingBlock (by default)
    expect(wrapper.vm.editingBlock).toEqual(
      wrapper.vm.$props.editorData.blocks[0]
    )
  })

  it('editingQuestion currentQuestion null computed test', () => {
    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: 1,
          blocks: [
            {
              order: 1,
              title: 'Block 1',
              questionData: {
                currentQuestion: null,
                questions: [
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 4',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
          ],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that if no question is current, then null
    expect(wrapper.vm.editingQuestion).toEqual(null)
  })

  it('editingQuestion currentQuestion valid computed test', () => {
    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: 1,
          blocks: [
            {
              order: 1,
              title: 'Block 1',
              questionData: {
                currentQuestion: 3,
                questions: [
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 2',
                    required: true,
                    order: 2,
                  },
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 3',
                    required: true,
                    order: 3,
                  },
                  {
                    type: 'multi-choice',
                    title: 'Default Question Title 1',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
          ],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Test that editingQuestion is currentQuestion in currentBlock (when all valid)
    expect(wrapper.vm.editingQuestion).toEqual(
      wrapper.vm.$props.editorData.blocks[0].questionData.questions[1]
    )
  })

  /* SIMPLE EMIT FUNCTION TESTS */

  // Create a shallow mount of the ThePanelPase vue file
  // const emit_wrapper = shallowMount(ThePanelBase, {
  //     propsData: {
  //         editorData: {
  //             currentBlock: 1,
  //             blocks: [{
  //                 order: 1,
  //                 questionData: {
  //                     currentQuestion: null,
  //                 },
  //             }, ],
  //         },
  //     },
  //     mocks: {
  //         $t: () => {}
  //     }
  // })

  // it('handleRequiredToggle function test', () => {

  //     // Call the handleRequiredToggle function to move to current page
  //     emit_wrapper.vm.handleRequiredToggle();

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handleRequiredToggle[0]).toEqual([]);

  // })

  // it('handleLikesToggle function test', () => {
  //     // Call the handleLikesToggle function to move to current page
  //     emit_wrapper.vm.handleLikesToggle();

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handleLikesToggle[0]).toEqual([]);

  // })

  // it('handleCommentsToggle function test', () => {
  //     // Call the handleCommentsToggle function to move to current page
  //     emit_wrapper.vm.handleCommentsToggle();

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handleCommentsToggle[0]).toEqual([]);

  // })

  // it('handleSharesToggle function test', () => {
  //     // Call the handleSharesToggle function to move to current page
  //     emit_wrapper.vm.handleSharesToggle();

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handleSharesToggle[0]).toEqual([]);

  // })

  // it('handleValidationToggle function test', () => {
  //     // Call the handleValidationToggle function to move to current page
  //     emit_wrapper.vm.handleValidationToggle();

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handleValidationToggle[0]).toEqual([]);

  // })

  it('handleQuestionType function test', () => {
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

    // // Create a shallow mount of the thePanelBase vue file
    // const special_wrapper = shallowMount(ThePanelBase, {
    //     propsData: {
    //         editorData: {
    //             currentBlock: store.getters["currentBlock"],
    //             blocks: store.getters["blocks"]
    //         },
    //     },
    //     mocks: {
    //         $t: () => {}
    //     }

    // })

    // Create a shallow mount of the ThePanelPase vue file
    const wrapper = shallowMount(ThePanelBase, {
      propsData: {
        editorData: {
          currentBlock: 1,
          blocks: [
            {
              order: 1,
              title: 'Block 1',
              questionData: {
                currentQuestion: 3,
                questions: [
                  {
                    type: 'News Post',
                    title: 'Default Question Title 2',
                    required: true,
                    order: 2,
                  },
                  {
                    type: 'Multiple Choice',
                    title: 'Default Question Title 3',
                    required: true,
                    order: 3,
                  },
                  {
                    type: 'Button Row',
                    title: 'Default Question Title 1',
                    required: true,
                    order: 1,
                  },
                ],
              },
            },
          ],
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    // Call the handleQuestionType function to move to current page
    wrapper.vm.handleQuestionType({
      options: ['News post', 'Button Row', 'Multiple Choice'],
      index: 0,
    })

    //console.log(emit_wrapper.emitted())

    // Test that the selected option is emitted
    expect(store.getters['currentQuestion'].type).toEqual('News post')
  })

  // it('handlePostStyle function test', () => {
  //     // Call the handlePostStyle function to move to current page
  //     emit_wrapper.vm.handlePostStyle("style");

  //     console.log(emit_wrapper.emitted())

  //     // Test that the selected option is emitted
  //     expect(emit_wrapper.emitted().handlePostStyle[0]).toEqual(["style"]);

  // })
})
