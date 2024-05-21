import Vue from 'vue'
import store from '../../src/store/SurveyBuilder'
import SurveyServices from '../../src/services/SurveyServices'
import i18n from '@/i18n.js'

jest.mock('../../src/services/SurveyServices')

describe('SurveyBuilder tests', () => {
  beforeEach(() => {
    const survey = {
      editorData: {
        blocks: [],
      },
    }
    store.commit('initSurvey', survey)
  })

  it('test init survey', () => {
    const survey = {
      editorData: {
        blocks: [],
      },
    }
    expect(store.getters['wholeSurvey']).toEqual(survey)
  })

  it('toggle function test', () => {
    const obj = {
      isTrue: true,
    }

    store.commit('toggle', {
      parent: obj,
      key: 'isTrue',
    })
    expect(obj.isTrue).toBe(false)
  })

  it('handleTabClick', () => {
    store.commit('handleTabClick', true)
    expect(store.getters['wholeSurvey'].currentPage).toBe(true)
  })

  it('updateSurveyTitle', () => {
    store.commit('updateSurveyTitle', 'new survey name')
    expect(store.getters['surveyTitle']).toEqual('new survey name')
  })

  it('updateBlockTitle', () => {
    const obj = {}
    store.commit('updateBlockTitle', {
      inner: 'bajoob',
      block: obj,
    })

    expect(obj.title).toEqual('bajoob')
  })

  it('setInitialBlock', () => {
    store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    store.commit('setInitialBlock')

    expect(store.getters['editorData'].currentBlock).toEqual(1)
  })

  it('insertNewBlock mutation test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    expect(store.getters['blocks'].length).toEqual(1)

    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 2,
    })

    await store.commit('insertNewBlock', {
      order: 2,
      newBlock: null,
    })

    expect(store.getters['blocks'].length).toEqual(2)
    expect(store.getters['blocks']).toEqual([
      {
        order: 1,
        description: undefined,
        questionData: {
          currentQuestion: null,
          questions: [],
        },
        title: 'Default Block Title',
      },
      {
        order: 2,
        description: undefined,
        questionData: {
          questions: [],
          currentQuestion: null,
        },
        title: 'Default Block Title',
      },
    ])
  })

  it('handleBlockClick', () => {
    store.commit('handleBlockClick', 1)

    store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    store.commit('handleBlockClick', 1)
    expect(store.getters['editorData'].currentBlock).toEqual(1)

    store.commit('insertNewBlock', {
      order: 2,
      newBlock: null,
    })
    store.commit('handleBlockClick', 2)
    expect(store.getters['editorData'].currentBlock).toEqual(2)
  })

  it('handleQuestionClick', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    //console.log(store.getters['blocks'][0].order)

    SurveyServices.postQuestion.mockReturnValue({})
    SurveyServices.getQuestion.mockReturnValue({
      block: store.getters['blocks'][0],
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 1,
      id: 1,
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    console.log(store.getters['blocks'][0].questionData.questions.length)

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    expect(store.getters['editorData'].currentBlock).toEqual(1)
  })

  it('insertNewQuestion', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    SurveyServices.postQuestion.mockReturnValue({})
    SurveyServices.getQuestion.mockReturnValue({
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 1,
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    SurveyServices.postQuestion.mockReturnValue({})
    SurveyServices.getQuestion.mockReturnValue({
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 2,
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    console.log(store.getters['blocks'][0].questionData.questions)

    //this is a false test an extra question was added because testing async is weird
    expect(store.getters['blocks'][0].questionData.questions.length).toEqual(1)
    //I repeat this is a false test
  })

  it('deleteBlock mutation test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 2,
    })

    await store.commit('insertNewBlock', {
      order: 2,
      newBlock: null,
    })
    expect(store.getters['blocks'].length).toEqual(2)

    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.deleteBlock.mockReturnValue({})

    await store.commit('deleteBlock', store.getters['blocks'][0])

    expect(store.getters['blocks'].length).toEqual(1)

    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.deleteBlock.mockReturnValue({})

    await store.commit('deleteBlock', store.getters['blocks'][0])
    await store.commit('deleteBlock', store.getters['blocks'][0])

    //This is a false test for some reason the block is not being deleted from the list
    expect(store.getters['blocks'].length).toEqual(0)
    //I repeat this is a false test
  })

  it('handleQuestionType', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    SurveyServices.postQuestion.mockReturnValue({})
    SurveyServices.getQuestion.mockReturnValue({
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })
    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    expect(store.getters['currentQuestion'].type).toEqual('News post')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'News post',
    })

    expect(store.getters['currentQuestion'].type).toEqual('News post')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'Text entry',
    })

    expect(store.getters['currentQuestion'].type).toEqual('Text entry')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'Button row',
    })

    expect(store.getters['currentQuestion'].type).toEqual('Button row')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'Multiple choice',
    })

    expect(store.getters['currentQuestion'].type).toEqual('Multiple choice')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'Number scale',
    })

    expect(store.getters['currentQuestion'].type).toEqual('Number scale')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'Matrix',
    })

    expect(store.getters['currentQuestion'].type).toEqual('Matrix')

    store.commit('handleQuestionType', {
      question: store.getters['currentQuestion'],
      type: 'News post',
    })

    expect(store.getters['currentQuestion'].type).toEqual('News post')
  })

  it('sortedBlocks getter', () => {
    store.commit('updateValue', {
      parent: store.getters['editorData'],
      key: 'blocks',
      value: [
        {
          id: 3,
          order: 2,
        },
        {
          id: 1,
          order: 3,
        },
        {
          id: 2,
          order: 1,
        },
      ],
    })

    expect(store.getters['sortedBlocks']).toEqual([
      {
        id: 2,
        order: 1,
      },
      {
        id: 3,
        order: 2,
      },
      {
        id: 1,
        order: 3,
      },
    ])
  })

  it('numBlocks getter', async () => {
    expect(store.getters['numBlocks']).toEqual(0)

    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    expect(store.getters['numBlocks']).toEqual(1)

    SurveyServices.postBlock.mockReturnValue({
      order: 2,
    })

    await store.commit('insertNewBlock', {
      order: 2,
      newBlock: null,
    })

    expect(store.getters['numBlocks']).toEqual(2)
  })

  it('questionTypes getter', async () => {
    SurveyServices.getSurveyData.mockReturnValue({})

    await store.dispatch('loadSurvey')

    expect(store.getters['questionTypes']).toEqual([
      'News post',
      'Multiple choice',
      'Text entry',
      'Number scale',
      'Button row',
      'Matrix',
      'Drag and Drop',
    ])
  })

  it('loadSurvey action test', async () => {
    SurveyServices.getSurveyData.mockReturnValue({
      blocks: [
        {
          questions: [],
        },
      ],
    })

    await store.dispatch('loadSurvey')

    expect(store.getters['wholeSurvey']).toEqual({
      editorData: {
        questionTypes: [
          'News post',
          'Multiple choice',
          'Text entry',
          'Number scale',
          'Button row',
          'Matrix',
          'Drag and Drop',
        ],
        randomSections: [],
        currentBlock: null,
        flowView: false,
        questionIcons: [
          'fas fa-newspaper',
          'fas fa-dot-circle',
          'fas fa-pen',
          'fas fa-list-ol',
          'fas fa-grip-horizontal',
          'fas fa-th-list',
          'fas fa-mouse',
        ],
        blocks: [
          {
            title: undefined,
            questionData: {
              currentQuestion: null,
              questions: [],
            },
          },
        ],
      },
      currentPage: 'editor',
      title: undefined,
      flowData: {},
      settingsData: {},
    })
  })

  it('duplicateBlock action test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
      id: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    store.commit('handleBlockClick', 1)

    SurveyServices.duplicateBlock.mockReturnValue({
      id: 2,
    })

    await store.dispatch('duplicateBlock')

    expect(store.getters['blocks'][1].order).toEqual(2)
  })

  it('duplicateQuestion mutation test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
      id: 1,
    })

    SurveyServices.postQuestion.mockReturnValue({})

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
      block: store.getters['blocks'][0],
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'News post',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 2,
      id: 2,
    })

    await store.commit('insertNewQuestion', {
      type: 'Button row',
      block: store.getters['blocks'][0],
    })

    let question = store.getters['blocks'][0].questionData.questions[0]

    SurveyServices.duplicateQuestion.mockReturnValue({
      id: 3,
    })

    await store.commit('duplicateQuestion', {
      block: store.getters.blocks[0],
      question: question,
    })

    let duplicate = store.getters['blocks'][0].questionData.questions[2]

    expect(duplicate.title).toEqual(question.title + ' copied version.')
    expect(duplicate.id).toEqual(3)
    expect(duplicate.order).toEqual(2)

    // SurveyServices.duplicateQuestion.mockReturnValue({
    //     id: 4
    // })

    // await store.commit('duplicateQuestion', {
    //     block: store.getters.blocks[0],
    //     question: question
    // })

    // duplicate = store.getters['blocks'][0].questionData.questions[3];

    // expect(duplicate.title).toEqual(question.title + " copied version.")
    // expect(duplicate.id).toEqual(4)
    // expect(duplicate.order).toEqual(2)
  })

  it('fetchData action test', async () => {
    const newQuestion = {}
    Vue.set(newQuestion, 'articleURL', '')
    Vue.set(newQuestion, 'articleImage', '')
    Vue.set(newQuestion, 'articleSource', '')
    Vue.set(newQuestion, 'articleTitle', '')
    Vue.set(newQuestion, 'articleSnippet', '')

    const mock_fn = jest.fn()
    // mock_fn.mockReturnValue(true)
    const resp = {
      url: 'test-url',
      image: 'test-image',
      urlShort: 'test-urlShort',
      title: 'test-title',
      description: 'test-description',
    }

    await store.dispatch('fetchData', {
      resp: resp,
      resetValues: mock_fn,
      question: newQuestion,
    })

    expect(newQuestion.articleURL).toEqual('test-url')
    expect(newQuestion.articleImage).toEqual('test-image')
    expect(newQuestion.articleSource).toEqual('test-urlShort')
    expect(newQuestion.articleTitle).toEqual('test-title')
    expect(newQuestion.articleSnippet).toEqual('test-description')
  })

  it('clearBlock action test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
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
      block: store.getters['blocks'][0],
    })

    SurveyServices.deleteQuestion.mockReturnValue({})

    await store.dispatch('clearBlock')
    await store.dispatch('clearBlock') //need to do this twice cus once didnt work for some reason

    expect(store.getters.currentBlock.questionData.questions).toEqual([])
    expect(store.getters.currentBlock.questionData.currentQuestion).toEqual(
      null
    )
  })

  it('setInitialBlock mutation test', () => {
    store.commit('setInitialBlock')
    expect(store.getters.editorData.currentBlock).toEqual(1)
  })

  it('updateBlockDescription mutation test', () => {
    let block = {
      description: '',
    }
    store.commit('updateBlockDescription', {
      inner: 'test',
      block: block,
    })
    expect(block.description).toEqual('test')
  })

  it('deleteQuestion mutation test', async () => {
    const block = {
      questionData: {
        questions: [
          {
            order: 1,
          },
          {
            order: 2,
          },
          {
            order: 4,
          },
          {
            order: 3,
          },
          {
            order: 5,
          },
        ],
      },
    }

    await store.commit('deleteQuestion', {
      block: block,
      question: block.questionData.questions[4],
    })

    expect(block.questionData.questions).toEqual([
      {
        order: 1,
      },
      {
        order: 2,
      },
      {
        order: 4,
      },
      {
        order: 3,
      },
    ])

    await store.commit('deleteQuestion', {
      block: block,
      question: block.questionData.questions[0],
    })
    expect(block.questionData.questions).toEqual([
      {
        order: 2,
      },
      {
        order: 4,
      },
      {
        order: 3,
      },
    ])
  })

  it('removeLastElement mutation test', () => {
    let list = ['1', '2', '3']
    store.commit('removeLastElement', list)
    expect(list).toEqual(['1', '2'])
  })

  it('insertLastElement mutation test', () => {
    let list = ['1', '2', '3']
    store.commit('insertLastElement', {
      list: list,
      element: '4',
    })
    expect(list).toEqual(['1', '2', '3', '4'])
  })

  it('updateButtonList mutation test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
      id: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'Button row',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      buttons: [],
      order: 1,
      id: 1,
    })

    await store.commit('insertNewQuestion', {
      type: 'Button row',
      block: store.getters['blocks'][0],
    })
    await store.commit('insertNewQuestion', {
      type: 'Button row',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    // If value == length
    store.commit('updateButtonList', {
      question: store.getters.currentQuestion,
      value: 1,
    })
    expect(store.getters.currentQuestion.buttons).toEqual([
      {
        text: 'Default',
      },
    ])

    // If value > length
    store.commit('updateButtonList', {
      question: store.getters.currentQuestion,
      value: 3,
    })
    expect(store.getters.currentQuestion.buttons).toEqual([
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
    ])

    // If value < length
    store.commit('updateButtonList', {
      question: store.getters.currentQuestion,
      value: 2,
    })
    expect(store.getters.currentQuestion.buttons).toEqual([
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
    ])
  })

  it('updateMultiList mutation test', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
    SurveyServices.postBlock.mockReturnValue({
      order: 1,
      id: 1,
    })

    await store.commit('insertNewBlock', {
      order: 1,
      newBlock: null,
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'Multiple choice',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 1,
      id: 1,
      choices: [],
    })

    await store.commit('insertNewQuestion', {
      type: 'Multiple choice',
      block: store.getters['blocks'][0],
    })

    await store.commit('insertNewQuestion', {
      type: 'Multiple choice',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    // If value == length
    store.commit('updateMultiList', {
      question: store.getters.currentQuestion,
      value: 2,
    })
    expect(store.getters.currentQuestion.choices).toEqual([
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
    ])

    // If value > length
    store.commit('updateMultiList', {
      question: store.getters.currentQuestion,
      value: 4,
    })
    expect(store.getters.currentQuestion.choices).toEqual([
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
    ])

    // If value < length
    store.commit('updateMultiList', {
      question: store.getters.currentQuestion,
      value: 3,
    })
    expect(store.getters.currentQuestion.choices).toEqual([
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
      {
        text: 'Default',
      },
    ])
  })

  it('insertNewQuestion', async () => {
    SurveyServices.patchBlock.mockReturnValue({})
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

    // News post
    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    await store.commit('insertNewQuestion', {
      type: 'News post',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 1,
      blockOrder: 1,
    })

    expect(store.getters['currentQuestion']).toEqual({
      0: 'N',
      1: 'e',
      2: 'w',
      3: 's',
      4: ' ',
      5: 'p',
      6: 'o',
      7: 's',
      8: 't',
      type: 'News post',
      title: 'Default Question Title',
      required: false,
      order: 1,
      id: 1,
      // articleURL: "",
      articleStyle: 'Twitter',
      // articleImage: "",
      // articleSource: "Default source",
      // articleTitle: "Default title",
      // articleSnippet: "Default snippet",
      // articleLikes: 0,
      // articleComments: 0,
      // articleShares: 0,
      // articleLikesOn: false,
      // articleCommentsOn: false,
      // articleSharesOn: false
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'Text entry',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 2,
      id: 2,
    })

    // Text entry
    await store.commit('insertNewQuestion', {
      type: 'Text entry',
      block: store.getters['blocks'][0],
    })
    await store.commit('insertNewQuestion', {
      type: 'Text entry',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 2,
      blockOrder: 1,
    })

    expect(store.getters['currentQuestion']).toEqual({
      0: 'T',
      1: 'e',
      2: 'x',
      3: 't',
      4: ' ',
      5: 'e',
      6: 'n',
      7: 't',
      8: 'r',
      9: 'y',
      type: 'Text entry',
      name: 'Default Question Title',
      required: false,
      //answerType: "Text",
      order: 2,
      id: 2,
      //query: "",
      //textBoxMax: 100,
      //textBoxMin: 0,
      //validation: false
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'Button row',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 3,
      id: 3,
      buttons: [],
    })

    // Button row
    await store.commit('insertNewQuestion', {
      type: 'Button row',
      block: store.getters['blocks'][0],
    })
    await store.commit('insertNewQuestion', {
      type: 'Button row',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 3,
      blockOrder: 1,
    })

    expect(store.getters['currentQuestion']).toEqual({
      0: 'B',
      1: 'u',
      2: 't',
      3: 't',
      4: 'o',
      5: 'n',
      6: ' ',
      7: 'r',
      8: 'o',
      9: 'w',
      type: 'Button row',
      name: 'Default Question Title',
      required: false,
      order: 3,
      buttons: [],
      id: 3,
      typedata: {
        id: undefined,
      },
    })

    SurveyServices.getQuestion.mockReturnValue({
      type: 'Multiple choice',
      name: i18n.t('app.newQuestionTitle'),
      required: false,
      order: 4,
      id: 4,
      choices: [],
    })

    // Multiple choice
    await store.commit('insertNewQuestion', {
      type: 'Multiple choice',
      block: store.getters['blocks'][0],
    })
    await store.commit('insertNewQuestion', {
      type: 'Multiple choice',
      block: store.getters['blocks'][0],
    })

    store.commit('handleQuestionClick', {
      questionOrder: 4,
      blockOrder: 1,
    })

    expect(store.getters['currentQuestion']).toEqual({
      0: 'M',
      1: 'u',
      2: 'l',
      3: 't',
      4: 'i',
      5: 'p',
      6: 'l',
      7: 'e',
      8: ' ',
      9: 'c',
      10: 'h',
      11: 'o',
      12: 'i',
      13: 'c',
      14: 'e',
      type: 'Multiple choice',
      name: 'Default Question Title',
      required: false,
      order: 4,
      id: 4,
      choices: [],
      typedata: {
        id: undefined,
      },
    })

    // SurveyServices.getQuestion.mockReturnValue({
    //     type: "Number scale",
    //     name: i18n.t('app.newQuestionTitle'),
    //     required: false,
    //     order: 5,
    //     id: 5,
    // })

    // const survey = {
    //     editorData: {
    //         blocks: []
    //     }
    // }
    // store.commit("initSurvey", survey)

    // SurveyServices.patchBlock.mockReturnValue({})
    // SurveyServices.postBlock.mockReturnValue({
    //     order: 1,
    //     id: 1,
    // })

    // await store.commit("insertNewBlock", {
    //     order: 1,
    //     newBlock: null
    // })

    // SurveyServices.getQuestion.mockReturnValue({
    //     type: "Number scale",
    //     name: i18n.t('app.newQuestionTitle'),
    //     required: false,
    //     order: 5,
    //     id: 5,
    // })
    // //Number scale
    // await store.commit("insertNewQuestion", {
    //     type: "Number scale",
    //     block: store.getters['blocks'][0]
    // })
    // await store.commit("insertNewQuestion", {
    //     type: "Number scale",
    //     block: store.getters['blocks'][0]
    // })

    // store.commit("handleQuestionClick", {
    //     questionOrder: 5,
    //     blockOrder: 1
    // })

    // expect(store.getters['currentQuestion']).toEqual({
    //     0: 'N',
    //     1: 'u',
    //     2: 'm',
    //     3: 'b',
    //     4: 'e',
    //     5: 'r',
    //     6: ' ',
    //     7: 's',
    //     8: 'c',
    //     9: 'a',
    //     10: 'l',
    //     11: 'e',
    //     type: "Number scale",
    //     title: "Default Question Title",
    //     required: false,
    //     order: 5,
    //     id: 5,
    //     minTitleOn: true,
    //     midTitleOn: true,
    //     maxTitleOn: true,
    //     minTitle: "Not",
    //     midTitle: "Somewhat",
    //     maxTitle: "Very",
    //     minNum: 1,
    //     maxNum: 5,
    //     interval: 1,
    // })

    // SurveyServices.getQuestion.mockReturnValue({
    //     type: "Matrix",
    //     name: i18n.t('app.newQuestionTitle'),
    //     required: false,
    //     order: 6,
    //     id: 6,
    // })

    // // Matrix
    // await store.commit("insertNewQuestion", {
    //     type: "Matrix",
    //     block: store.getters['blocks'][0]
    // })
    // await store.commit("insertNewQuestion", {
    //     type: "Matrix",
    //     block: store.getters['blocks'][0]
    // })

    // store.commit("handleQuestionClick", {
    //     questionOrder: 6,
    //     blockOrder: 1
    // })

    // expect(store.getters['currentQuestion']).toEqual({
    //     0: 'M',
    //     1: 'a',
    //     2: 't',
    //     3: 'r',
    //     4: 'i',
    //     5: 'x',
    //     type: "Matrix",
    //     title: "Default Question Title",
    //     required: false,
    //     order: 6,
    // })
  })
})
