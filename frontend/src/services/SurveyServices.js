import axios from 'axios'
import { devServer, publicPath } from '../../vue.config'
const baseUrl = devServer.proxy + 'api'
// const baseUrl = "https://cp13demoapi.piran.xyz/api"

const getSurveys = async () => {
  await axios.get(baseUrl + '/surveys/researcher/1').then((res) => {
    return res.data
  })
}

const getCollaborators = async (id) => {
  const response =  await axios.get(devServer.proxy + 'survey' + `/collaborators/survey/${id}`)
  return response.data
}

const getToken = async (email) => {
  try {
    const response = await axios.get(devServer.proxy + 'account/get_token/?email=' + email)
    return response.data.token;
  } catch (error) {
    console.error('Error getting token:', error);
    throw error;
  }
}


const publishSurveyAnswer = async (data) => {
  const response = await axios.post(baseUrl + '/st/survey/saveResponse', data)
  return response.data.Message
}

const getSurveyCode = async (id) => {
  const response = await axios.post(baseUrl + `/surveys/code/${id}`)
  return response.data.code
}

const getSurveyQuestions = async (code) => {
  const response = await axios.get(baseUrl + `/st/surveyQuestions/${code}`)
  return response.data.id
}

const addSurvey = async (data) => {
  const response = await axios.post(baseUrl + '/surveys', data)
  return response.data
}

//step 2
const getSurvey = async (id) => {
  const response = await axios.get(baseUrl + `/surveys/${id}`)
  return response.data
}

const getSurveyData = async (id) => {
  const response = await axios.get(baseUrl + `/surveys/${id}/data`)
  return response.data
}

const deleteSurvey = async (id) => {
  const response = await axios.delete(baseUrl + `/surveys/${id}`)
  return response.data
}

const cloneSurvey = async (survey_id, user_id, language) => {
  const response = await axios.post(
    devServer.proxy + `survey/cloneSurvey/${survey_id}/${user_id}/${language}`
  )
  return response.data
}

const getQuestions = async (id) => {
  const response = await axios.get(baseUrl + `/blocks/${id}/questions`)
  return response.data
}

const getQuestion = async (id) => {
  const response = await axios.get(baseUrl + `/questions/${id}`)
  return response.data
}

const getLinkInformation = async (data) => {
  const response = await axios.post(baseUrl + `/article`, data)
  return response.data
}

const getVideoLinkInformation = async (link) => {
  const response = await axios.get(baseUrl + `/video?link=${link}`)
  return response.data
}

const postBlock = async (id, data) => {
  const response = await axios.post(baseUrl + `/surveys/${id}/blocks`, data)
  return response.data
}

const patchBlock = async (id, data) => {
  const response = await axios.patch(baseUrl + `/blocks/${id}`, data)
  return response.data
}

const deleteBlock = async (id) => {
  await axios.delete(baseUrl + `/blocks/${id}`)
}

const patchSurvey = async (id, data) => {
  const response = await axios.patch(baseUrl + `/surveys/${id}`, data)
  return response.data
}

const postQuestion = async (id, data) => {
  const response = await axios.post(baseUrl + `/blocks/${id}/questions`, data)
  return response.data
}

const duplicateQuestion = async (id, data) => {
  const response = await axios.post(
    baseUrl + `/questions/duplicate/${id}`,
    data
  )
  return response.data
}

const duplicateBlock = async (id, data) => {
  const response = await axios.post(baseUrl + `/blocks/duplicate/${id}`, data)
  return response.data
}

const patchQuestion = async (id, data) => {
  const response = await axios.patch(baseUrl + `/questions/${id}`, data)
  return response.data
}

const patchQuestionType = async (id, data) => {
  const response = await axios.patch(baseUrl + `/questions/inner/${id}`, data)
  return response.data
}

const patchQuestionImage = async (id, data) => {
  const response = await axios.patch(baseUrl + `/questions/image/${id}`, data)
  return response.data
}

const patchTextAnswerType = async (id, data) => {
  const response = await axios.patch(
    baseUrl + `/questions/textentry/${id}`,
    data
  )
  return response.data
}

const deleteQuestion = async (id) => {
  const response = await axios.delete(baseUrl + `/questions/${id}`)
  return response.data
}

const postMultiChoiceQuestion = async (id, data) => {
  const response = await axios.post(baseUrl + `/questions/multi/${id}`, data)
  return response.data
}
const postRankOrderQuestion = async (id, data) => {
  const response = await axios.post(baseUrl + `/questions/rank/${id}`, data)
  return response.data
}

const postButtonRowQuestion = async (id, data) => {
  const response = await axios.post(
    baseUrl + `/questions/buttonrow/${id}`,
    data
  )
  return response.data
}

const postPostAddonfield = async (id, data) => {
  const response = await axios.post(
    baseUrl + `/questions/postaddonfield/${id}`,
    data
  )
  return response.data
}

const deleteMultiChoiceQuestion = async (id, temp) => {
  const response = await axios.delete(baseUrl + `/questions/multi/${id}`, {
    data: temp,
  })
  return response.data
}

const deleteRankOrderQuestion = async (id, temp) => {
  const response = await axios.delete(baseUrl + `/questions/rank/${id}`, {
    data: temp,
  })
  return response.data
}

const deleteButtonQuestion = async (id, temp) => {
  const response = await axios.delete(baseUrl + `/questions/buttonrow/${id}`, {
    data: temp,
  })
  return response.data
}

const deletepostPostAddonfield = async (id, temp) => {
  const response = await axios.delete(
    baseUrl + `/questions/postaddonfield/${id}`,
    { data: temp }
  )
  return response.data
}

const patchMultiChoiceQuestion = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/questions/multi/${id}`, temp)
  return response.data
}

const patchRankOrderQuestion = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/questions/rank/${id}`, temp)
  return response.data
}

const patchMultiChoiceAnswers = async (id, temp) => {
  const response = await axios.patch(
    baseUrl + `/questions/multiChoice/${id}`,
    temp
  )
  return response.data
}
const patchMatrixTableAnswers = async (id, temp) => {
  const response = await axios.patch(
    baseUrl + `/questions/matrixTable/${id}`,
    temp
  )
  return response.data
}
const patchSlidersAnswers = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/questions/sliders/${id}`, temp)
  return response.data
}
const patchGroupsAnswers = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/questions/groups/${id}`, temp)
  return response.data
}

const patchButtonRowQuestion = async (id, temp) => {
  const response = await axios.patch(
    baseUrl + `/questions/buttonrow/${id}`,
    temp
  )
  return response.data
}

const patchNumberScale = async (id, temp) => {
  const response = await axios.patch(
    baseUrl + `/questions/numberScale/${id}`,
    temp
  )
  return response.data
}

const patchPostAddonfield = async (id, temp) => {
  const response = await axios.patch(
    baseUrl + `/questions/postaddonfield/${id}`,
    temp
  )
  return response.data
}

const patchUpdateOrder = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/blocks/${id}`, temp)
  return response.data
}

const patchRandomSections = async (id, temp) => {
  const response = await axios.patch(baseUrl + `/randomSections/${id}`, temp)
  return response.data
}

const postRandomSections = async (id, order, temp) => {
  const response = await axios.post(
    baseUrl + `/randomSections?order=${order}&survey_id=${id}`
  )
  return response.data
}

const getRandomFiveResults = async (id) => {
  const response = await axios.get(
    baseUrl + `/st/survey/result/statistic/random/${id}`
  )
  return response.data
}
const getLastFiveResults = async (id) => {
  const response = await axios.get(
    baseUrl + `/st/survey/result/statistic/last/${id}`
  )
  return response.data
}

const patchMatrixTableQuestion = async (data) => {
  const response = await axios.patch(
    baseUrl + `/questions/patchMatrixTableQuestion`,
    data
  )
  return response.data
}
const patchSlidersQuestion = async (data) => {
  const response = await axios.patch(
    baseUrl + `/questions/patchSlidersQuestion`,
    data
  )
  return response.data
}
const patchGroupsQuestion = async (data) => {
  const response = await axios.patch(
    baseUrl + `/questions/patchGroupsQuestion`,
    data
  )
  return response.data
}

const postComment = async (id, data) => {
  const response = await axios.post(baseUrl + `/questions/comment/${id}`, data)
  return response.data
}
const delComment = async (id, data) => {
  const response = await axios.delete(baseUrl + `/questions/comment/${id}`)
  return response.data
}
const patchComment = async (id, data) => {
  const response = await axios.patch(baseUrl + `/questions/comment/${id}`, data)
  return response.data
}
const postAvatar = async (data) => {
  const response = await axios.post(baseUrl + `/common/avatar`, data)
  return response.data
}
const deleteAvatar = async (data) => {
  const response = await axios.delete(baseUrl + `/common/avatar?id=${data.id}`)
  return response.data
}
const getAvatar = async (data) => {
  const response = await axios.get(baseUrl + `/common/avatar?user=${data.user}`)
  return response.data
}

export default {
  patchButtonRowQuestion,
  postButtonRowQuestion,
  patchMultiChoiceQuestion,
  patchRankOrderQuestion,
  deleteMultiChoiceQuestion,
  deleteRankOrderQuestion,
  deleteButtonQuestion,
  postMultiChoiceQuestion,
  postRankOrderQuestion,
  deleteQuestion,
  patchQuestion,
  patchQuestionType,
  patchTextAnswerType,
  duplicateQuestion,
  getQuestion,
  postQuestion,
  getSurveys,
  addSurvey,
  getSurvey,
  postPostAddonfield,
  getQuestions,
  deleteSurvey,
  cloneSurvey,
  getSurveyData,
  getLinkInformation,
  getVideoLinkInformation,
  deletepostPostAddonfield,
  duplicateBlock,
  postBlock,
  patchBlock,
  deleteBlock,
  patchSurvey,
  patchPostAddonfield,
  patchUpdateOrder,
  patchRandomSections,
  postRandomSections,
  publishSurveyAnswer,
  getSurveyCode,
  getSurveyQuestions,
  patchMultiChoiceAnswers,
  patchMatrixTableAnswers,
  patchNumberScale,
  patchQuestionImage,
  getRandomFiveResults,
  getLastFiveResults,
  patchMatrixTableQuestion,
  // updateRank,
  postComment,
  delComment,
  patchComment,
  patchSlidersQuestion,
  patchSlidersAnswers,
  patchGroupsAnswers,
  patchGroupsQuestion,
  postAvatar,
  deleteAvatar,
  getAvatar,
  getCollaborators,
  getToken,
}
