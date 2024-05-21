<template>
  <div class="question-box" :style="color">
    <div class="title">
      <h1>
        Q{{ number + 1 }}<span style="color: red" v-show="requiredShow">*</span>
      </h1>
      <p class="title">{{ questionData.title }}</p>
    </div>
    <PostTwitterReadOnly v-if="questionData.articleStyle === 'Twitter'" @updateAnswer="getData" :question="questionData">
    </PostTwitterReadOnly>
    <PostFacebookReadOnly v-else-if="questionData.articleStyle === 'Facebook'" @updateAnswer="getData"
      :question="questionData"></PostFacebookReadOnly>
    <PostMixReadOnly v-else-if="questionData.articleStyle === 'Mix'" @updateAnswer="getData" :question="questionData">
    </PostMixReadOnly>
    <PostInstagramReadOnly v-else-if="questionData.articleStyle === 'Instagram'" @updateAnswer="getData"
      :question="questionData"></PostInstagramReadOnly>
    <YouTubeReadOnly ref="youtubeid" v-else-if="questionData.articleStyle === 'Youtube'" @updateAnswer="getData"
      :question="questionData"></YouTubeReadOnly>
    <TikTokReadOnly ref="tiktokid" v-else-if="questionData.articleStyle === 'TikTok'" @updateAnswer="getData"
      :question="questionData"></TikTokReadOnly>
    <PostRedditReadOnly v-else-if="questionData.articleStyle === 'Reddit'" @updateAnswer="getData"
      :question="questionData"></PostRedditReadOnly>
    <PostLinkedinReadOnly v-else-if="questionData.articleStyle === 'Linkedin'" @updateAnswer="getData"
      :question="questionData"></PostLinkedinReadOnly>
    <PostTumblrReadOnly v-else-if="questionData.articleStyle === 'Tumblr'" @updateAnswer="getData"
      :question="questionData"></PostTumblrReadOnly>
    <PostPinterestReadOnly v-else-if="questionData.articleStyle === 'Pinterest'" @updateAnswer="getData"
      :question="questionData"></PostPinterestReadOnly>
    <PostQuoraReadOnly v-else-if="questionData.articleStyle === 'Quora'" @updateAnswer="getData" :question="questionData">
    </PostQuoraReadOnly>
    <div v-if="questionData.articleStyle !== 'Instagram'">
      <div v-for="item in question.comments || []" :key="item.id" class="comment-item">
        <el-avatar style="flex-shrink: 0" :key="item.avatarUrl" :src="item.avatarUrl"></el-avatar>
        <div style="margin-left: 10px; width: 100%">
          <p style="font-size: 12px">{{ item.username }}</p>
          <p>{{ item.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PostTwitterReadOnly from '@/components/SurveyTaker/PostTwitterReadOnly'
import PostFacebookReadOnly from '@/components/SurveyTaker/PostFacebookReadOnly'
import PostInstagramReadOnly from '@/components/SurveyTaker/PostInstagramReadOnly'
import YouTubeReadOnly from '@/components/SurveyTaker/YouTubeReadOnly'
import TikTokReadOnly from '@/components/SurveyTaker/TikTokReadOnly'
import PostLinkedinReadOnly from '@/components/SurveyTaker/PostLinkedinReadOnly'
import PostTumblrReadOnly from '@/components/SurveyTaker/PostTumblrReadOnly'
import PostPinterestReadOnly from '@/components/SurveyTaker/PostPinterestReadOnly'
import PostRedditReadOnly from './PostRedditReadOnly.vue'
import PostMixReadOnly from '@/components/SurveyTaker/PostMixReadOnly'
import PostQuoraReadOnly from "@/components/SurveyTaker/PostQuoraReadOnly.vue";

export default {
  props: {
    question: Object,
    index: Number,
  },
  name: 'NewsPost',
  components: {
    PostFacebookReadOnly,
    PostTwitterReadOnly,
    YouTubeReadOnly,
    TikTokReadOnly,
    PostInstagramReadOnly,
    PostLinkedinReadOnly,
    PostTumblrReadOnly,
    PostPinterestReadOnly,
    PostRedditReadOnly,
    PostMixReadOnly,
    PostQuoraReadOnly,
  },
  data() {
    return {
      questionData: '',
      number: 0,

      requiredShow: false,
      color: '',

      resultObj: {
        question_id: 0,
        response_question_answer: [
          {
            title: '',
            answerText: null,
            answerDecimal: 0,
          },
        ],
      },
    }
  },
  created() {
    console.log('NEW POST TESTING', this.question)
    this.resultObj.question_id = this.question.question
    this.number = this.index
    this.questionData = this.question
    this.requiredShow = this.questionData.required
    this.sendResult()
  },
  methods: {
    getData(answer) {
      this.resultObj.response_question_answer = answer
      this.resultObj.question_id = this.questionData.id
      this.sendResult()
    },

    sendResult() {
      console.log('NEW POST', this.resultObj, 'Number: ', this.number)
      this.$emit('updateQuestion', this.resultObj, this.number)
    },

    changeColor(color) {
      if (color) {
        this.color = ''
      } else {
        this.color = 'border:1px solid red'
      }
    },

    checkValidity() {
      if (this.questionData.required === true) {
        let flag = false
        for (
          let i = 0;
          i < this.resultObj.response_question_answer.length;
          i++
        ) {
          if (this.resultObj.response_question_answer[i].answerText != null) {
            flag = true
          }
        }
        if (flag === true) {
          this.changeColor(true)
          return true
        } else {
          this.changeColor(false)
          return false
        }
      } else {
        this.changeColor(true)
        if (this.questionData.articleStyle === 'Youtube') {
          this.$refs['youtubeid'].stopPlay()
        }
        return true
      }
    },
  },
}
</script>

<style scoped>
.question-box {
  border: 2px solid #eff2f5;
  border-radius: 4px;
  background: white;
  padding: 8px;
  width: auto;
}
@media (min-width: 1130px) {
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    text-align: left;
    margin-right: 8px;
    font-size: 30px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: larger;
    font-weight: bold;
  }
}
@media (max-width: 1129px) and (min-width: 890px) {
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    font-size: 25px;
    text-align: left;
    margin-right: 8px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: large;
    font-weight: bold;
  }
}
@media (max-width: 889px) {
  .question-box {
    margin: 2px;
    padding: 0px;
  }
  h1 {
    color: black;
    padding: 0 0 0 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-style: normal;
    font-weight: bold;
    font-size: 20px;
    text-align: left;
    margin-right: 8px;
  }
  .title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    white-space: normal;
    word-wrap: break-word;
    font-family: Arial, Helvetica, sans-serif;
    font-size: small;
    font-weight: bold;
  }
}

.comment-item {
  display: flex;
  margin-bottom: 10px;
}

.comment-item p {
  margin: 0 10px;
}
</style>
