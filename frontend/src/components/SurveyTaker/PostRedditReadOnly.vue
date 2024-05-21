<template>
  <div class="out-box">
    <h1>
      {{ question.articleTitle }}
    </h1>
    <div class="post">
      <a :href="question.articleURL" target="_blank" v-if="isImage"
        ><img
          :src="question.articleImage"
          :alt="question.articleTitle"
          width="100%"
          height="auto"
      /></a>
      <div v-else class="no-image">{{ $t('postEditable.noImage') }}</div>
      <div class="post-bottom">
        <p>{{ question.articleSource }}</p>
        <a
          class="btn-open"
          :href="question.articleURL"
          style="text-decoration: none; color: #7f7f7f"
          target="_blank"
          >Open</a
        >
      </div>
    </div>

    <el-row class="btn-row" style="margin: 10px">
      <!--like-->
      <el-col :style="colWidth" v-show="likeShow">
        <div
          @click="clickItem('Like')"
          :style="iconColorLike"
          class="clickItem-like"
          :title="likeTitle"
        >
          <span class="iconfont clickItem-icon-like"
            ><svg
              t="1684996466584"
              class="icon-like"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="5852"
              width="15"
              height="15"
            >
              <path
                d="M688.64 995.2H341.12a53.12 53.12 0 0 1-53.12-52.48V520.96H45.44a32 32 0 0 1-30.08-21.12 30.72 30.72 0 0 1 8.32-35.2L512 21.76a32 32 0 0 1 44.16 0l442.88 442.24a33.92 33.92 0 0 1 7.04 35.84 32 32 0 0 1-30.08 19.84h-215.68v402.56a71.68 71.68 0 0 1-71.68 72.96z m-336-64h336a7.04 7.04 0 0 0 7.04-7.04V488.32a32 32 0 0 1 32.64-32h172.16L535.04 90.88 128 456.32h192a32 32 0 0 1 32.64 32z"
                fill="#323333"
                p-id="5853"
              ></path></svg
          ></span>
          <span class="clickItem-title-like" :style="textColorLike">{{
            this.questionData.articleLikes
          }}</span>
        </div>
      </el-col>

      <!--reply-->
      <el-col :style="colWidth" v-show="replyShow">
        <div
          @click="clickItem('Reply')"
          :style="iconColorReply"
          class="clickItem-reply"
          title="Reply"
        >
          <span class="iconfont clickItem-icon-reply">&#xe602;</span>
          <span class="clickItem-title-reply" :style="textColorReply">{{
            this.questionData.articleComments
          }}</span>
        </div>
      </el-col>

      <!--share-->
      <el-col :style="colWidth" v-show="shareShow">
        <div
          @click="clickItem('Share')"
          :style="iconColorShare"
          class="clickItem-share"
          :title="shareTitle"
        >
          <span class="iconfont clickItem-icon-share">&#xe60b;</span>
          <!-- <span class="clickItem-title-share" :style="textColorShare">{{
            this.questionData.articleShares
          }}</span> -->
          <span>Share</span>
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
      <span style="color: red">{{ $t('surveyTaker.tips') }}</span>
      {{ $t('surveyTaker.tipHint') }}
    </span>
  </div>
</template>

<script>
import store from '../../store/SurveyBuilder.js'

export default {
  name: 'PostTwitterReadOnly',
  store: store,
  props: {
    question: Object,
  },
  data() {
    return {
      questionData: '',
      shareTitle: 'Share',
      likeTitle: 'Like',

      iconColorReply: '',
      textColorReply: '',
      iconColorShare: '',
      textColorShare: '',
      iconColorLike: '',
      textColorLike: '',
      iconColorAdd1: '',
      textColorAdd1: '',
      iconColorAdd2: '',
      textColorAdd2: '',

      replyShow: false,
      shareShow: false,
      likeShow: false,
      addon1Show: false,
      addon2Show: false,

      inputReplyShow: false,
      inputShareShow: false,
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

    checkShare() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Share') {
          this.answerObj[i].answerText = 'selected'
        }
      }
    },

    cancelCheckShare() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Share') {
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
      this.shareShow = this.questionData.articleSharesOn
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

    clickItem(item) {
      if (item === 'Reply') {
        this.inputReplyShow = !this.inputReplyShow
        if (this.inputReplyShow === true) {
          this.questionData.articleComments++
          this.changeReplyColor(true)
          this.openReplyDialog()
        } else {
          this.changeReplyColor(false)
          this.questionData.articleComments--
          this.cancelCheckReply()
          this.sendResult()
        }
      }

      if (item === 'Share') {
        this.inputShareShow = !this.inputShareShow
        if (this.inputShareShow === true) {
          this.questionData.articleShares++
          this.changeShareColor(true)
          this.checkShare()
          this.sendResult()
        } else {
          this.questionData.articleShares--
          this.changeShareColor(false)
          this.cancelCheckShare()
          this.sendResult()
        }
      }

      if (item === 'Like') {
        this.inputLikeShow = !this.inputLikeShow
        if (this.inputLikeShow === true) {
          this.questionData.articleLikes++
          this.changeLikeColor(true)
          this.checkLike()
          this.sendResult()
        } else {
          this.questionData.articleLikes--
          this.changeLikeColor(false)
          this.cancelCheckLike()
          this.sendResult()
        }
      }

      if (item === 'Add1') {
        this.add1Flag = !this.add1Flag
        if (this.add1Flag === true) {
          this.add1Count++
          this.changeAdd1Color(true)
          this.openAdd1Dialog()
        } else {
          this.add1Count--
          this.changeAdd1Color(false)
          this.cancelCheckAdd1()
          this.sendResult()
        }
      }

      if (item === 'Add2') {
        this.add2Flag = !this.add2Flag
        if (this.add2Flag === true) {
          this.add2Count++
          this.changeAdd2Color(true)
          this.openAdd2Dialog()
        } else {
          this.add2Count--
          this.changeAdd2Color(false)
          this.cancelCheckAdd2()
          this.sendResult()
        }
      }
    },

    changeReplyColor(flag) {
      if (flag) {
        this.iconColorReply = 'color: #7f7f7f;background: #e6eef6;'
        this.textColorReply = 'color: #7f7f7f;'
      } else {
        this.iconColorReply = 'color: #7f7f7f;background: #FFFFFF;'
        this.textColorReply = 'color: #7f7f7f;'
      }
    },

    changeShareColor(flag) {
      if (flag) {
        this.iconColorShare = 'color: #7f7f7f;background: #e6eef6;'
        this.textColorShare = 'color: #7f7f7f;'
      } else {
        this.iconColorShare = 'color: #7f7f7f;background: #FFFFFF;'
        this.textColorShare = 'color: #7f7f7f;'
      }
    },

    addClickItems() {
      if (this.questionData.articleCommentsOn === true) {
        this.clickItems.push('Reply')
        this.countItems++
      }
      if (this.questionData.articleSharesOn === true) {
        this.clickItems.push('Share')
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
        // this.colWidth = 'width: 33.3%'
        this.colWidth = ''
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
      if (
        this.question.articleImage === '' ||
        this.question.articleImage == null
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

.no-image {
  background-color: #d1d9dd;
  height: 100px;
  width: 100%;
  color: black;
  text-align: center;
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

@font-face {
  font-family: 'iconfont'; /* Project id  */
  src: url('./fonts/iconfont.ttf?t=1650093070773') format('truetype');
}

.iconfont {
  font-family: 'iconfont' !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.btn-open {
  margin-right: 5px;
  margin-top: 2px;
  padding: 10px;
  border: 1px solid;
  border-color: #7f7f7f;
  border-radius: 30px;
}

.btn-row {
  display: flex;
  align-items: center;
}

.post-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clickItem-like,
.clickItem-reply,
.clickItem-share {
  border: 1px solid;
  border-radius: 30px;
  border-color: #7f7f7f;
  color: #7f7f7f;
}

.clickItem-like:hover,
.clickItem-reply:hover,
.clickItem-share:hover {
  background-color: #e6eef6;
}

@media (min-width: 1130px) {
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
    font-size: 25px;
    line-height: 30px;
  }

  .clickItem-reply {
    cursor: pointer;
    display: inline-block;
    text-align: center;
    padding: 4px;
    margin-top: 5px;
  }

  .clickItem-icon-reply {
    font-size: 15px;
    color: #7f7f7f;
    padding: 10px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    font-size: 15px;
    /* color: #479be9;
    background: #e6eef6; */
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-right: 5px;
    color: #7f7f7f;
    font-size: 15px;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 4px;
    margin-top: 5px;
    cursor: pointer;
  }

  .clickItem-icon-share {
    font-size: 15px;
    color: #7f7f7f;
    padding: 8px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    font-size: 15px;
    /* color: #53b681;
    background: #e6f1eb; */
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-left: 5px;
    color: #7f7f7f;
    font-size: 15px;
  }

  .clickItem-like {
    cursor: pointer;
    display: inline-block;
    text-align: center;
    padding: 4px;
    margin-top: 5px;
  }

  .clickItem-icon-like {
    font-size: 15px;
    color: #7f7f7f;
    padding: 10px;
    border-radius: 30px;
  }

  .clickItem-icon-like:hover {
    font-size: 15px;
    cursor: pointer;
    /* color: #e53b7f;
    background: #f5e4eb; */
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-right: 5px;
    color: #7f7f7f;
    font-size: 15px;
  }

  .clickItem-icon-like:hover + .clickItem-title-like {
    /* color: #e53b7f; */
    cursor: pointer;
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
}

@media (max-width: 1129px) and (min-width: 890px) {
  .out-box {
    width: 330px;
    overflow: hidden;
    margin: 0 auto;
  }

  .post {
    width: 320px;
    background-color: white;
    border: 1px solid #d1d9dd;
    margin: 0 auto;
    padding-bottom: 10px;
    border-radius: 14px;
    overflow: hidden;
  }

  .btn-open {
    font-size: 12px;
  }

  .icon-like {
    width: 13px;
    height: 13px;
  }

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 12px;
    line-height: 13px;
    text-align: left;

    color: #65676b;
    margin: 3px 10px 0px;
  }

  h1,
  h2 {
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    font-style: normal;
    font-weight: 600;
    font-size: 10px;
    line-height: 13px;
    text-align: left;
    margin: 3px 10px 2px;
  }

  span {
    font-size: 12px;
  }

  .clickItem-reply {
    cursor: pointer;
    display: inline-block;
    text-align: center;
    padding: 3px;
  }

  .clickItem-icon-reply {
    font-size: 12px;
    color: #7f7f7f;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    font-size: 12px;
    /* color: #479be9;
    background: #e6eef6; */
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-right: 4px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 3px;
    cursor: pointer;
  }

  .clickItem-icon-share {
    font-size: 12px;
    color: #7f7f7f;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    font-size: 12px;
    /* color: #53b681;
    background: #e6f1eb; */
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-left: 4px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-like {
    cursor: pointer;
    display: inline-block;
    text-align: center;
    padding: 3px;
  }

  .clickItem-icon-like {
    font-size: 12px;
    color: #7f7f7f;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-like:hover {
    font-size: 12px;
    cursor: pointer;
    /* color: #e53b7f;
    background: #f5e4eb; */
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-right: 4px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-icon-like:hover + .clickItem-title-like {
    /* color: #e53b7f; */
    cursor: pointer;
  }

  .clickItem-add1 {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-add1 {
    font-size: 12px;
    color: #7f7f7f;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-add1:hover {
    font-size: 12px;
    color: #479be9;
    background: #e6eef6;
  }

  .clickItem-title-add1 {
    font-family: inherit;
    margin-left: 4px;
    color: #7f7f7f;
    font-size: 12px;
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
    font-size: 12px;
    color: #7f7f7f;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-add2:hover {
    font-size: 12px;
    color: #53b681;
    background: #e6f1eb;
  }

  .clickItem-title-add2 {
    font-family: inherit;
    margin-left: 4px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-icon-add2:hover + .clickItem-title-add2 {
    color: #53b681;
  }

  .tip-box {
    font-size: 9px;
    color: #6e6e6e;
    margin: 6px;
    padding: 6px;
  }
}

@media (max-width: 889px) {
  .out-box {
    width: 320px;
    overflow: hidden;
    margin: 0 auto;
  }

  .post {
    width: 320px;
    background-color: white;
    border: 1px solid #d1d9dd;
    margin: 0 auto;
    padding-bottom: 10px;
    border-radius: 14px;
    overflow: hidden;
  }

  .btn-open {
    font-size: 10px;
  }

  .icon-like {
    width: 11px;
    height: 11px;
  }

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 10px;
    line-height: 6px;
    text-align: left;

    color: #65676b;
    margin: 3px 8px 1px;
  }

  h1,
  h2 {
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    font-style: normal;
    font-weight: 550;
    font-size: 12px;
    line-height: 10px;
    text-align: left;
    margin: 2px 8px 1px;
  }

  span {
    font-size: 10px;
  }

  .clickItem-reply {
    cursor: pointer;
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-reply {
    font-size: 10px;
    color: #7f7f7f;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    font-size: 10px;
    /* color: #479be9;
    background: #e6eef6; */
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-right: 3px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 2px;
    cursor: pointer;
  }

  .clickItem-icon-share {
    font-size: 10px;
    color: #7f7f7f;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    font-size: 10px;
    /* color: #53b681;
    background: #e6f1eb; */
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-left: 3px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-like {
    display: inline-block;
    text-align: center;
    padding: 2px;
    cursor: pointer;
  }

  .clickItem-icon-like {
    font-size: 10px;
    color: #7f7f7f;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-like:hover {
    font-size: 10px;
    /* color: #e53b7f;
    background: #f5e4eb; */
    cursor: pointer;
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-right: 3px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-icon-like:hover + .clickItem-title-like {
    /* color: #e53b7f; */
    cursor: pointer;
  }

  .clickItem-add1 {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-add1 {
    font-size: 10px;
    color: #7f7f7f;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-add1:hover {
    font-size: 10px;
    color: #479be9;
    background: #e6eef6;
  }

  .clickItem-title-add1 {
    font-family: inherit;
    margin-left: 3px;
    color: #7f7f7f;
    font-size: 10px;
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
    font-size: 10px;
    color: #7f7f7f;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-add2:hover {
    font-size: 10px;
    color: #53b681;
    background: #e6f1eb;
  }

  .clickItem-title-add2 {
    font-family: inherit;
    margin-left: 3px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-icon-add2:hover + .clickItem-title-add2 {
    color: #53b681;
  }

  .tip-box {
    font-size: 10px;
    color: #6e6e6e;
    margin: 4px;
    padding: 4px;
  }
}
</style>
