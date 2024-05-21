import { shallowMount } from '@vue/test-utils'
import store from '../../src/store/SurveyBuilder'
import QuestionContentArticles from '../../src/components/SurveyBuilder/QuestionContentArticles.vue'
import SurveyServices from '../../src/services/SurveyServices'

jest.mock('../../src/services/SurveyServices')

describe('Question Content Articles test', () => {
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

  it('updateImage function test', () => {
    // Create a shallow mount of the QuestionContentArticles vue file
    const wrapper = shallowMount(QuestionContentArticles, {
      propsData: {
        data: {},
      },
      mocks: {
        $t: () => {},
      },
    })

    // Call the updateImage function
    wrapper.vm.updateImage({
      target: {
        value: 'New Image',
      },
    })

    // Test this.imageURL is updated
    expect(wrapper.vm.$data.imageURL).toEqual('New Image')
  })

  it('fetchData function test', async () => {
    // Create a shallow mount of the QuestionContentArticles vue file
    const wrapper = shallowMount(QuestionContentArticles, {
      propsData: {
        data: store.getters.currentQuestion,
        articleURL: 'blank',
        imageURL: 'blink',
      },
      mocks: {
        $t: () => {},
      },
    })

    SurveyServices.getLinkInformation.mockReturnValue({
      url: 'test-url',
      image: 'test-image',
      urlShort: 'test-urlShort',
      title: 'test-title',
      description: 'test-description',
    })

    wrapper.vm.fetchData()

    console.log(wrapper.vm.$props)

    expect(wrapper.vm.$props.data.articleImage).toEqual('')
  })

  // it('fetchData function test', async () => {
  //     // Create a shallow mount of the QuestionContentArticles vue file
  //     const wrapper = shallowMount(QuestionContentArticles, {
  //         propsData: {
  //             data: {
  //                 articleURL: "sample.com",
  //                 articleImage: "original.png"
  //             }
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the fetchData function
  //     await wrapper.vm.fetchData();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().fetchData[0][0]).toMatchObject({
  //         url: wrapper.vm.$data.articleURL,
  //         resetValues: expect.any(Function)

  //     });

  //     // Test anonymous function passed as resetValues
  //     await wrapper.setProps({data: {articleImage: "new.png"}});

  //     expect(wrapper.vm.$data.imageURL).toEqual("original.png")

  //     // Call the anonymous resetValues function
  //     wrapper.emitted().fetchData[0][0].resetValues();

  //     // Test that imageURL is updated
  //     expect(wrapper.vm.$data.imageURL).toEqual("new.png")

  // })

  // it('refreshImage function test', () => {
  //     // Create a shallow mount of the QuestionContentArticles vue file
  //     const wrapper = shallowMount(QuestionContentArticles, {
  //         propsData: {
  //             data: {
  //                 articleImage: "image.com",
  //             }
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the refreshImage function
  //     wrapper.vm.refreshImage();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().refreshImage[0]).toEqual(["image.com"]);

  // })

  // it('updateLikes function test', () => {
  //     // Create a shallow mount of the QuestionContentArticles vue file
  //     const wrapper = shallowMount(QuestionContentArticles, {
  //         propsData: {
  //             data: {
  //                 likeCount: 123,
  //             }
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateLikes function
  //     wrapper.vm.updateLikes();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateLikes[0]).toEqual([123]);

  // })

  // it('updateComments function test', () => {
  //     // Create a shallow mount of the QuestionContentArticles vue file
  //     const wrapper = shallowMount(QuestionContentArticles, {
  //         propsData: {
  //             data: {
  //                 commentCount: 1234,
  //             }
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateComments function
  //     wrapper.vm.updateComments();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateComments[0]).toEqual([1234]);

  // })

  // it('updateShares function test', () => {
  //     // Create a shallow mount of the QuestionContentArticles vue file
  //     const wrapper = shallowMount(QuestionContentArticles, {
  //         propsData: {
  //             data: {
  //                 shareCount: 12345,
  //             }
  //         },
  //         mocks: {
  //             $t: () => {}
  //         }
  //     })

  //     // Call the updateShares function
  //     wrapper.vm.updateShares();

  //     console.log(wrapper.emitted())

  //     // Test parameter is emitted
  //     expect(wrapper.emitted().updateShares[0]).toEqual([12345]);

  // })

  it('resetValues function test', async () => {
    // Create a shallow mount of the QuestionContentArticles vue file
    const wrapper = shallowMount(QuestionContentArticles, {
      propsData: {
        data: {
          articleImage: 'original.png',
        },
      },
      mocks: {
        $t: () => {},
      },
    })

    await wrapper.setProps({ data: { articleImage: 'new.png' } })

    expect(wrapper.vm.$data.imageURL).toEqual('original.png')

    // Call the resetValues function
    wrapper.vm.resetValues()

    // Test that imageURL is updated
    expect(wrapper.vm.$data.imageURL).toEqual('new.png')
  })
})
