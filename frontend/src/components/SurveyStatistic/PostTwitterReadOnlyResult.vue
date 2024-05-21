<template>
  <div class="out-box">
    <div class="post">
      <a :href="question.typedata.articleURL" v-if="isImage"
        ><img
          :src="question.typedata.articleImageLink"
          :alt="question.typedata.articleTitle"
          width="100%"
          height="auto"
      /></a>

      <youtube
        v-else-if="this.questionData.typedata.articleStyle === 'Youtube'"
        :width="youtubeWidth"
        :height="youtubeHeight"
        :resize="true"
        class="youtube"
        :video-id="question.articleSource"
        ref="youtube"
      ></youtube>
      <div v-else class="no-image">{{ $t('postEditable.noImage') }}</div>
      <h1>
        <a
          :href="question.typedata.articleURL"
          style="text-decoration: none; color: black"
          >{{ question.typedata.articleTitle }}</a
        >
      </h1>
      <h2>
        {{ question.typedata.articleSnippet }}
      </h2>
      <p>{{ question.typedata.articleSource }}</p>
    </div>

    <el-row style="margin: 10px">
      <!--reply-->
      <el-col :style="colWidth" v-show="replyShow">
        <div class="clickItem-reply" title="Reply">
          <i
            class="el-icon-chat-round clickItem-icon-reply"
            :style="iconColorReply"
            @click="clickItem('Reply')"
          ></i>
          <span class="clickItem-title-reply" :style="textColorReply">{{
            this.questionData.typedata.articleComments
          }}</span>
        </div>
      </el-col>

      <!--retweet-->
      <el-col :style="colWidth" v-show="retweetShow">
        <div class="clickItem-retweet" :title="retweetTitle">
          <i
            class="el-icon-share clickItem-icon-retweet"
            :style="iconColorRetweet"
          ></i>
          <!--          <i class="el-icon-share clickItem-icon-retweet" :style="iconColorRetweet" @click="clickItem('Retweet')"></i>-->
          <span class="clickItem-title-retweet" :style="textColorRetweet">{{
            this.questionData.typedata.articleShares
          }}</span>
        </div>
      </el-col>

      <!--like-->
      <el-col :style="colWidth" v-show="likeShow">
        <div class="clickItem-like" :title="likeTitle">
          <i
            class="el-icon-star-off clickItem-icon-like"
            :style="iconColorLike"
          ></i>
          <!--          <i class="el-icon-star-off clickItem-icon-like" :style="iconColorLike" @click="clickItem('Like')"></i>-->
          <span class="clickItem-title-like" :style="textColorLike">{{
            this.questionData.typedata.articleLikes
          }}</span>
        </div>
      </el-col>

      <!--add1-->
      <el-col :style="colWidth" v-show="addon1Show">
        <div class="clickItem-add1" :title="add1Title">
          <i
            class="clickItem-icon-add1"
            :class="add1Icon"
            :style="iconColorAdd1"
            @click="clickItem('Add1')"
          ></i>
          <span class="clickItem-title-add1" :style="textColorAdd1">{{
            add1Count
          }}</span>
        </div>
      </el-col>

      <!--add2-->
      <el-col :style="colWidth" v-show="addon2Show">
        <div class="clickItem-add2" :title="add2Title">
          <i
            class="clickItem-icon-add2"
            :class="add2Icon"
            :style="iconColorAdd2"
            @click="clickItem('Add2')"
          ></i>
          <span class="clickItem-title-add2" :style="textColorAdd2">{{
            add2Count
          }}</span>
        </div>
      </el-col>
    </el-row>

    <span class="tip-box" v-if="questionData.required === true">
      <span style="color: red">Tips:</span> Please click at least one button.
    </span>
  </div>
</template>

<script>
import store from '../../store/SurveyBuilder.js'
import SurveyServices from '../../services/SurveyServices'

export default {
  name: 'PostTwitterReadOnlyResult',
  store: store,
  props: {
    question: Object,
  },
  data() {
    return {
      questionData: '',
      retweetTitle: 'Retweet',
      likeTitle: 'Like',

      iconColorReply: '',
      textColorReply: '',
      iconColorRetweet: '',
      textColorRetweet: '',
      iconColorLike: '',
      textColorLike: '',
      iconColorAdd1: '',
      textColorAdd1: '',
      iconColorAdd2: '',
      textColorAdd2: '',

      replyShow: false,
      retweetShow: false,
      likeShow: false,
      addon1Show: false,
      addon2Show: false,

      inputReplyShow: false,
      inputRetweetShow: false,
      inputLikeShow: false,
      add1Flag: false,
      add2Flag: false,

      colWidth: '',
      countItems: 0,
      clickItems: [],

      add1Title: '',
      add1Icon: '',
      add1Count: '',

      add2Title: '',
      add2Icon: '',
      add2Count: '',
      windowWidth: document.documentElement.clientWidth,
      youtubeWidth: '',
      youtubeHeight: '',
      answerObj: [
        {
          title: '',
          answerText: null,
          answerDecimal: null,
        },
      ],
    }
  },

  methods: {
    checkBtnSize() {
      if (this.windowWidth > 1130) {
        this.youtubeWidth = '420px'
        this.youtubeHeight = '300px'
      } else if (this.windowWidth < 889) {
        this.youtubeWidth = '256px'
        this.youtubeHeight = '144px'
      } else {
        this.youtubeWidth = '533px'
        this.youtubeHeight = '300px'
      }
      console.log(this.windowWidth)
    },
    initializeAnswer() {
      for (let i = 0; i < this.countItems; i++) {
        this.answerObj[i] = {
          title: this.clickItems[i],
          answerText: null,
          answerDecimal: null,
        }
      }
    },

    sendResult() {
      this.$emit('updateAnswer', this.answerObj)
    },

    openReplyDialog() {
      this.$prompt('', 'Tweet your reply', {
        confirmButtonText: 'Submit',
        cancelButtonText: 'Cancel',
        inputErrorMessage: 'Please input something',
        inputValidator: (val) => {
          if (val === null) {
            return false
          }
        },
      })
        .then(({ value }) => {
          for (let i = 0; i < this.countItems; i++) {
            if (this.answerObj[i].title === 'Reply') {
              this.answerObj[i].answerText = value
            }
          }
          this.sendResult()
          this.$message({
            type: 'success',
            message: 'Success reply',
          })
        })
        .catch(() => {
          this.cancelCheckReply()
          this.changeReplyColor(false)
          this.question.articleComments--
          this.inputReplyShow = false

          this.$message({
            type: 'info',
            message: 'Cancel',
          })
        })
    },

    cancelCheckReply() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Reply') {
          this.answerObj[i].answerText = ''
        }
      }
    },

    openRetweetDialog() {
      this.$prompt('Add a comment', 'Quote Tweet', {
        confirmButtonText: 'Submit',
        cancelButtonText: 'Cancel',
        inputErrorMessage: 'Please input something',
        inputValidator: (val) => {
          if (val === null) {
            return false
          }
        },
      })
        .then(({ value }) => {
          for (let i = 0; i < this.countItems; i++) {
            if (this.answerObj[i].title === 'Retweet') {
              this.answerObj[i].answerText = value
            }
          }
          this.sendResult()
          this.$message({
            type: 'success',
            message: 'Success retweet',
          })
        })
        .catch(() => {
          this.cancelCheckRetweet()
          this.changeRetweetColor(false)
          this.question.articleShares--
          this.inputRetweetShow = false

          this.$message({
            type: 'info',
            message: 'Cancel',
          })
        })
    },

    cancelCheckRetweet() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Retweet') {
          this.answerObj[i].answerText = ''
        }
      }
    },

    openAdd1Dialog() {
      this.$prompt('', 'Please input something', {
        confirmButtonText: 'Submit',
        cancelButtonText: 'Cancel',
        inputErrorMessage: 'Please input something',
        inputValidator: (val) => {
          if (val === null) {
            return false
          }
        },
      })
        .then(({ value }) => {
          for (let i = 0; i < this.countItems; i++) {
            if (this.answerObj[i].title === this.add1Title) {
              this.answerObj[i].answerText = value
            }
          }
          this.sendResult()
          this.$message({
            type: 'success',
            message: 'Success',
          })
        })
        .catch(() => {
          console.log(this.add1Flag)
          this.cancelCheckAdd1()
          this.changeAdd1Color(false)
          this.add1Count--
          this.add1Flag = false

          this.$message({
            type: 'info',
            message: 'Cancel',
          })
        })
    },

    cancelCheckAdd1() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === this.questionData.addon[0].title) {
          this.answerObj[i].answerText = ''
        }
      }
    },

    openAdd2Dialog() {
      this.$prompt('', 'Please input something', {
        confirmButtonText: 'Submit',
        cancelButtonText: 'Cancel',
        inputErrorMessage: 'Please input something',
        inputValidator: (val) => {
          if (val === null) {
            return false
          }
        },
      })
        .then(({ value }) => {
          for (let i = 0; i < this.countItems; i++) {
            if (this.answerObj[i].title === this.add2Title) {
              this.answerObj[i].answerText = value
            }
          }
          this.sendResult()
          this.$message({
            type: 'success',
            message: 'Success',
          })
        })
        .catch(() => {
          this.cancelCheckAdd2()
          this.changeAdd2Color(false)
          this.add2Count--
          this.add2Flag = false

          this.$message({
            type: 'info',
            message: 'Cancel',
          })
        })
    },

    cancelCheckAdd2() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === this.add2Title) {
          this.answerObj[i].answerText = ''
        }
      }
    },

    checkLike() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Like') {
          this.answerObj[i].answerText = 'selected'
        }
      }
    },

    cancelCheckLike() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Like') {
          this.answerObj[i].answerText = ''
        }
      }
    },

    checkShow() {
      this.replyShow = this.questionData.articleCommentsOn
      this.retweetShow = this.questionData.articleSharesOn
      this.likeShow = this.questionData.articleLikesOn
      if (this.questionData.addon.length === 1) {
        this.addon1Show = true
        this.add1Title = this.questionData.addon[0].title
        this.add1Icon = this.questionData.addon[0].icon
        this.add1Count = this.questionData.addon[0].count
      }
      if (this.questionData.addon.length === 2) {
        this.addon1Show = true
        this.addon2Show = true

        this.add1Title = this.questionData.addon[0].title
        this.add1Icon = this.questionData.addon[0].icon
        this.add1Count = this.questionData.addon[0].count
        this.add2Title = this.questionData.addon[1].title
        this.add2Icon = this.questionData.addon[1].icon
        this.add2Count = this.questionData.addon[1].count
      }
    },

    clickItem(item, flag) {
      if (item === 'Reply') {
        this.$emit('changeValue', this.questionData.comments, 1)
      }
      if (item === 'Add1') {
        this.$emit('changeValue', this.questionData.addon[0].text, 2)
        //this.$emit("changeValue",["Here is a test"]);
      }
      if (item === 'Add2') {
        this.$emit('changeValue', this.questionData.addon[1].text, 3)
      }
    },

    changeReplyColor(flag) {
      if (flag === true) {
        this.iconColorReply =
          'font-size:15px; color: #479BE9; background: #E6EEF6;'
        this.textColorReply = 'color: #479BE9;'
      } else {
        this.iconColorReply = ''
        this.textColorReply = ''
      }
    },

    changeRetweetColor(flag) {
      if (flag === true) {
        this.iconColorRetweet =
          'font-size:15px; color: #53B681;background: #E6F1EB;'
        this.textColorRetweet = 'color: #53B681;'
        this.retweetTitle = 'Undo Retweet'
      } else {
        this.iconColorRetweet = ''
        this.textColorRetweet = ''
        this.retweetTitle = 'Retweet'
      }
    },
    changeLikeColor(flag) {
      if (flag === true) {
        this.iconColorLike =
          'font-size:15px; color: #E53B7F;background: #F5E4EB;'
        this.textColorLike = 'color: #E53B7F;'
        this.likeTitle = 'Unlike'
      } else {
        this.iconColorLike = ''
        this.textColorLike = ''
        this.likeTitle = 'Like'
      }
    },
    changeAdd1Color(flag) {
      if (flag === true) {
        this.iconColorAdd1 =
          'font-size:15px; color: #479BE9; background: #E6EEF6;'
        this.textColorAdd1 = 'color: #479BE9;'
      } else {
        this.iconColorAdd1 = ''
        this.textColorAdd1 = ''
      }
    },

    changeAdd2Color(flag) {
      if (flag === true) {
        this.iconColorAdd2 =
          'font-size:15px; color: #53B681;background: #E6F1EB;'
        this.textColorAdd2 = 'color: #53B681;'
      } else {
        this.iconColorAdd2 = ''
        this.textColorAdd2 = ''
      }
    },

    addClickItems() {
      if (this.questionData.articleCommentsOn === true) {
        this.clickItems.push('Reply')
        this.countItems++
      }
      if (this.questionData.articleSharesOn === true) {
        this.clickItems.push('Retweet')
        this.countItems++
      }
      if (this.questionData.articleLikesOn === true) {
        this.clickItems.push('Like')
        this.countItems++
      }

      if (this.questionData.addon.length != 0) {
        for (let i = 0; i < this.questionData.addon.length; i++) {
          this.clickItems.push(this.questionData.addon[i].title)
        }
        this.countItems = this.countItems + this.questionData.addon.length
      }
      if (this.countItems == 1) {
        this.colWidth = 'width: 100%'
      }
      if (this.countItems == 2) {
        this.colWidth = 'width: 50%'
      }
      if (this.countItems == 3) {
        this.colWidth = 'width: 33.3%'
      }
      if (this.countItems == 4) {
        this.colWidth = 'width: 25%'
      }
      if (this.countItems == 5) {
        this.colWidth = 'width: 20%'
      }
    },
  },

  created() {
    this.questionData = this.question
    this.questionData.articleComments = this.question.comments.length
    this.questionData.articleCommentsOn = this.question.typedata.articleCommentsOn
    this.questionData.articleImageLink = this.question.typedata.articleImageLink
    this.questionData.articleLikes = this.question.typedata.articleLikes
    this.questionData.articleLikesOn = this.question.typedata.articleLikesOn
    this.questionData.articleShares = this.question.typedata.articleShares
    this.questionData.articleSharesOn = this.question.typedata.articleSharesOn
    this.questionData.articleSnippet = this.question.typedata.articleSnippet
    this.questionData.articleSource = this.question.typedata.articleSource
    this.questionData.articleStyle = this.question.typedata.articleStyle
    this.questionData.articleTitle = this.question.typedata.articleTitle
    this.questionData.articleURL = this.question.typedata.articleURL
    this.questionData.numberAddon = this.question.typedata.numberAddon
    this.questionData.question = this.question.typedata.question
    this.questionData.id = this.question.typedata.id
    this.checkBtnSize()
    this.addClickItems()
    this.checkShow()
    this.initializeAnswer()
  },

  computed: {
    /**
     * Check whether it is an image or not
     * @returns {boolean} false if not an image and true if it is
     */
    isImage() {
      console.log('Question Data: ', this.questionData)
      if (
        this.questionData.typedata.articleImageLink === '' ||
        this.questionData.typedata.articleImageLink == null
      ) {
        return false
      }

      return true
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: center;
}

.out-box {
  width: 430px;
  overflow: hidden;
  margin: 0 auto;
}

.post {
  width: 420px;
  background-color: white;
  border: 1px solid #d1d9dd;
  margin: 0 auto;
  padding-bottom: 10px;
  border-radius: 14px;
  overflow: hidden;
}

.no-image {
  background-color: #d1d9dd;
  height: 100px;
  width: 100%;
  color: black;
  text-align: center;
}

p {
  font-family: Helvetica, Arial, sans-serif;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 15px;
  text-align: left;

  color: #65676b;
  margin: 6px 12px 0px;
}

h1,
h2 {
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  font-style: normal;
  font-weight: 600;
  font-size: 14px;
  line-height: 16px;
  text-align: left;

  margin: 6px 12px 2px;
}

h1 {
  color: #101419;
  margin: 6px 12px 2px;
}

h2 {
  color: #566370;
  font-weight: 500;
  margin: 4px 12px 2px;
}

.clickItem-reply {
  display: inline-block;
  text-align: center;
  padding: 2px;
}

.clickItem-icon-reply {
  font-size: 15px;
  color: #7f7f7f;
  padding: 10px;
  border-radius: 30px;
}

.clickItem-icon-reply:hover {
  font-size: 15px;
  color: #479be9;
  background: #e6eef6;
}

.clickItem-title-reply {
  font-family: inherit;
  margin-left: 5px;
  color: #7f7f7f;
  font-size: 15px;
}

.clickItem-icon-reply:hover + .clickItem-title-reply {
  color: #479be9;
}

.clickItem-retweet {
  display: inline-block;
  text-align: center;
  padding: 2px;
}

.clickItem-icon-retweet {
  font-size: 15px;
  color: #7f7f7f;
  padding: 10px;
  border-radius: 30px;
}

.clickItem-icon-retweet:hover {
  font-size: 15px;
  color: #53b681;
  background: #e6f1eb;
}

.clickItem-title-retweet {
  font-family: inherit;
  margin-left: 5px;
  color: #7f7f7f;
  font-size: 15px;
}

.clickItem-icon-retweet:hover + .clickItem-title-retweet {
  color: #53b681;
}

.clickItem-like {
  display: inline-block;
  text-align: center;
  padding: 2px;
}

.clickItem-icon-like {
  font-size: 15px;
  color: #7f7f7f;
  padding: 10px;
  border-radius: 30px;
}

.clickItem-icon-like:hover {
  font-size: 15px;
  color: #e53b7f;
  background: #f5e4eb;
}

.clickItem-title-like {
  font-family: inherit;
  margin-left: 5px;
  color: #7f7f7f;
  font-size: 15px;
}

.clickItem-icon-like:hover + .clickItem-title-like {
  color: #e53b7f;
}

.clickItem-add1 {
  display: inline-block;
  text-align: center;
  padding: 2px;
}

.clickItem-icon-add1 {
  font-size: 15px;
  color: #7f7f7f;
  padding: 10px;
  border-radius: 30px;
}

.clickItem-icon-add1:hover {
  font-size: 15px;
  color: #479be9;
  background: #e6eef6;
}

.clickItem-title-add1 {
  font-family: inherit;
  margin-left: 5px;
  color: #7f7f7f;
  font-size: 15px;
}

.clickItem-icon-add1:hover + .clickItem-title-add1 {
  color: #479be9;
}

.clickItem-add2 {
  display: inline-block;
  text-align: center;
  padding: 2px;
}

.clickItem-icon-add2 {
  font-size: 15px;
  color: #7f7f7f;
  padding: 10px;
  border-radius: 30px;
}

.clickItem-icon-add2:hover {
  font-size: 15px;
  color: #53b681;
  background: #e6f1eb;
}

.clickItem-title-add2 {
  font-family: inherit;
  margin-left: 5px;
  color: #7f7f7f;
  font-size: 15px;
}

.clickItem-icon-add2:hover + .clickItem-title-add2 {
  color: #53b681;
}

.tip-box {
  font-size: 13px;
  color: #6e6e6e;
  margin: 8px;
  padding: 8px;
}
</style>
