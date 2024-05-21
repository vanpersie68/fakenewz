<template>
  <div class="out-box">
    <h1>{{ question.articleTitle }}</h1>
    <div class="content">
      <div class="post">
        <a
          v-if="question.articleImageLink"
          :href="question.articleURL"
          target="_blank"
          ><img
            :src="question.articleImageLink"
            :alt="question.articleImageLink"
            width="200px"
            height="auto"
        /></a>
        <div v-else class="no-image">{{ $t('postEditable.noImage') }}</div>
        <!-- <p>
          {{ question.articleSource.toUpperCase() }}
        </p> -->
        <el-row class="icon-row" style="margin: 10px">
          <!--like-->
          <el-col
            :style="colWidth"
            v-show="likeShow"
            style="text-align: center"
          >
            <div class="clickItem-like" :title="likeTitle">
              <span
                class="iconfont clickItem-icon-like"
                :style="iconColorLike"
                @click="clickItem('Like')"
                >&#xe8ab;</span
              >
              <div class="clickItem-title-like" :style="textColorLike">
                {{ this.questionData.articleLikes }}
              </div>
            </div>
          </el-col>
          <!--reply-->
          <el-col
            :style="colWidth"
            v-show="replyShow"
            style="text-align: center"
          >
            <div class="clickItem-reply" title="Reply">
              <span
                class="iconfont clickItem-icon-reply"
                :style="iconColorReply"
                @click="clickItem('Reply')"
                >&#xe602;</span
              >
              <div class="clickItem-title-reply" :style="textColorReply">
                {{ this.questionData.articleComments }}
              </div>
            </div>
          </el-col>
          <!--share-->
          <el-col
            :style="colWidth"
            v-show="shareShow"
            style="text-align: center"
          >
            <div class="clickItem-share" :title="shareTitle">
              <span
                class="iconfont clickItem-icon-share"
                :style="iconColorShare"
                @click="clickItem('Share')"
                >&#xe60b;</span
              >
              <div class="clickItem-title-share" :style="textColorShare">
                {{ this.questionData.articleShares }}
              </div>
            </div>
          </el-col>
          <!--add1-->
          <el-col
            :style="colWidth"
            v-show="addon1Show"
            style="text-align: center"
          >
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
          <el-col
            :style="colWidth"
            v-show="addon2Show"
            style="text-align: center"
          >
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
      </div>
    </div>

    <span class="tip-box" v-if="questionData.required === true">
      <span style="color: red">{{ $t('surveyTaker.tips') }}</span>
      {{ $t('surveyTaker.tipHint') }}
    </span>
  </div>
</template>

<script>
import Vue from 'vue'
import VueYoutube from 'vue-youtube'
import LineBase from '@/components/SurveyBuilder/LineBase'

Vue.use(VueYoutube)

export default {
  name: 'TikTokReadOnly',
  props: {
    question: Object,
  },
  components: {
    LineBase,
  },
  data() {
    return {
      questionData: '',
      shareTitle: 'Share',
      likeTitle: 'Like',
      showPlayer: true,
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

      playTime: 0,
      playStateCode: -1,
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

  created() {
    this.questionData = this.question
    this.checkBtnSize()
    this.addClickItems()
    this.checkShow()
    this.initializeAnswer()
    this.$emit('updateAnswer', this.answerObj)
  },

  computed: {
    player() {
      return this.$refs.youtube.player
    },
  },

  methods: {
    stopPlay() {
      this.showPlayer = false
    },

    checkBtnSize() {
      if (this.windowWidth > 1130) {
        this.youtubeWidth = '640px'
        this.youtubeHeight = '360px'
      } else if (this.windowWidth < 889) {
        this.youtubeWidth = '256px'
        this.youtubeHeight = '144px'
      } else {
        this.youtubeWidth = '533px'
        this.youtubeHeight = '300px'
      }
    },

    async addPlayInfo() {
      let playState = ''
      let time = 0
      let getCurrentTime = await this.$refs.youtube.player.getCurrentTime()
      time = getCurrentTime
      let getPlayerState = await this.$refs.youtube.player.getPlayerState()
      const handle = (result) => {
        if (result === -1) {
          playState = 'unstarted'
        } else if (result === 0) {
          playState = 'ended'
        } else if (result === 1) {
          playState = 'playing'
        } else if (result === 2) {
          playState = 'paused'
        } else if (result === 3) {
          playState = 'buffering'
        } else if (result === 5) {
          playState = 'video cued'
        }
      }
      handle(getPlayerState)
      this.answerObj[this.countItems].title = 'play_time(seconds)'
      this.answerObj[this.countItems].answerText = Math.ceil(time)
      this.answerObj[this.countItems].answerDecimal = Math.ceil(time)
    },

    initializeAnswer() {
      for (let i = 0; i < this.countItems; i++) {
        this.answerObj[i] = {
          title: this.clickItems[i],
          answerText: null,
          answerDecimal: null,
        }
      }
      this.answerObj[this.countItems] = {
        title: 'play_time(seconds)',
        answerText: 0,
        answerDecimal: 0,
      }
    },

    sendResult() {
      this.addPlayInfo()
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
          this.questionData.articleComments--
          this.changeReplyColor(false)
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
      // if (flag === true) {
      //   this.iconColorReply = 'color: #479BE9; background: #E6EEF6;'
      //   this.textColorReply = 'color: #479BE9;'
      // } else {
      //   this.iconColorReply = 'color: #7f7f7f;background: #FFFFFF;'
      //   this.textColorReply = 'color: #7f7f7f;'
      // }
    },

    // changeShareColor(flag) {
    //   if (flag === true) {
    //     this.iconColorShare = 'color: #53B681;background: #E6F1EB;'
    //     this.textColorShare = 'color: #53B681;'
    //     this.shareTitle = 'Undo Share'
    //   } else {
    //     this.iconColorShare = 'color: #7f7f7f;background: #FFFFFF;'
    //     this.textColorShare = 'color: #7f7f7f;'
    //     this.shareTitle = 'Share'
    //   }
    // },

    // changeLikeColor(flag) {
    //   if (flag === true) {
    //     this.iconColorLike = 'color: #E53B7F;background: #F5E4EB;'
    //     this.textColorLike = 'color: #E53B7F;'
    //     this.likeTitle = 'Unlike'
    //   } else {
    //     this.iconColorLike = 'color: #7f7f7f;background: #FFFFFF;'
    //     this.textColorLike = 'color: #7f7f7f;'
    //     this.likeTitle = 'Like'
    //   }
    // },

    changeAdd1Color(flag) {
      if (flag === true) {
        this.iconColorAdd1 = 'color: #479BE9; background: #E6EEF6;'
        this.textColorAdd1 = 'color: #479BE9;'
      } else {
        this.iconColorAdd1 = 'color: #7f7f7f;background: #FFFFFF;'
        this.textColorAdd1 = 'color: #7f7f7f;'
      }
    },

    changeAdd2Color(flag) {
      if (flag === true) {
        this.iconColorAdd2 = 'color: #53B681;background: #E6F1EB;'
        this.textColorAdd2 = 'color: #53B681;'
      } else {
        this.iconColorAdd2 = 'color: #7f7f7f;background: #FFFFFF;'
        this.textColorAdd2 = 'color: #7f7f7f;'
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
}
</script>

<style scoped>
.out-box {
  width: 100%;
  overflow: hidden;
  margin: 0 auto;
}

html:lang(ur) * {
  text-align: center;
}

.content {
  display: flex;
}

.post {
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  width: auto;
  background-color: white;
  margin: 0 auto;
  overflow: hidden;
  text-align: center;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.icon-row {
  display: flex;
  flex-direction: column;
  align-self: flex-end;
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

h1 {
  color: #101419;
  margin: 6px 12px 2px 6px;
  text-align: center;
}

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

img {
  border-radius: 7px;
}

/*下面的是按钮*/
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

@media (min-width: 1130px) {
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

    margin: 6px 12px 10px;
  }

  .clickItem-reply {
    display: inline-block;
    text-align: center;
    padding: 2px;
    margin-top: 5px;
  }

  .clickItem-icon-reply {
    font-size: 17px;
    color: #333;
    background-color: #c2bfbf;
    padding: 10px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    /* font-size: 15px; */
    /* color: #479be9; */
    /* background: #e6eef6; */
    cursor: pointer;
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-top: 10px;
    color: #7f7f7f;
    font-size: 15px;
  }

  .clickItem-icon-reply:hover + .clickItem-title-reply {
    /* color: #479be9; */
    cursor: pointer;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 2px;
    margin-top: 5px;
  }

  .clickItem-icon-share {
    font-size: 17px;
    /* color: #7f7f7f; */
    color: #333;
    background-color: #c2bfbf;
    padding: 10px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    /* font-size: 15px; */
    /* color: #53b681; */
    /* background: #e6f1eb; */
    cursor: pointer;
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-top: 10px;
    color: #7f7f7f;
    font-size: 15px;
  }

  .clickItem-icon-share:hover + .clickItem-title-share {
    /* color: #53b681; */
    cursor: pointer;
  }

  .clickItem-like {
    display: inline-block;
    text-align: center;
    padding: 2px;
    margin-top: 5px;
  }

  .clickItem-icon-like {
    font-size: 20px;
    padding: 10px;
    border-radius: 30px;
    color: #333;
    background-color: #c2bfbf;
  }

  .clickItem-icon-like:hover {
    /* font-size: 20px; */
    /* color: #e53b7f; */
    /* background: #f5e4eb; */
    cursor: pointer;
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-top: 10px;
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
  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 10px;
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

  .clickItem-reply {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-reply {
    font-size: 14px;
    color: #333;
    background-color: #c2bfbf;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    /* font-size: 12px; */
    /* color: #479be9; */
    /* background: #e6eef6; */
    cursor: pointer;
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-top: 7px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-icon-reply:hover + .clickItem-title-reply {
    /* color: #479be9; */
    cursor: pointer;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-share {
    font-size: 14px;
    /* color: #7f7f7f; */
    color: #333;
    background-color: #c2bfbf;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    /* font-size: 12px; */
    /* color: #53b681; */
    cursor: pointer;
    /* background: #e6f1eb; */
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-top: 7px;
    color: #7f7f7f;
    font-size: 12px;
  }

  .clickItem-icon-share:hover + .clickItem-title-share {
    /* color: #53b681; */
    cursor: pointer;
  }

  .clickItem-like {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-like {
    font-size: 15px;
    color: #333;
    background-color: #c2bfbf;
    padding: 6px;
    border-radius: 30px;
  }

  .clickItem-icon-like:hover {
    /* font-size: 12px; */
    /* color: #e53b7f; */
    /* background: #f5e4eb; */
    cursor: pointer;
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-top: 7px;
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

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 2px;
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
    font-size: 6px;
    line-height: 10px;
    text-align: left;

    margin: 2px 8px 1px;
  }

  .clickItem-reply {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-reply {
    font-size: 12px;
    color: #333;
    background-color: #c2bfbf;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-reply:hover {
    /* font-size: 10px; */
    /* color: #479be9; */
    /* background: #e6eef6; */
    cursor: pointer;
  }

  .clickItem-title-reply {
    font-family: inherit;
    margin-top: 4px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-icon-reply:hover + .clickItem-title-reply {
    /* color: #479be9; */
    cursor: pointer;
  }

  .clickItem-share {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-share {
    font-size: 12px;
    /* color: #7f7f7f; */
    color: #333;
    background-color: #c2bfbf;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-share:hover {
    /* font-size: 10px; */
    /* color: #53b681; */
    cursor: pointer;
    /* background: #e6f1eb; */
  }

  .clickItem-title-share {
    font-family: inherit;
    margin-top: 4px;
    color: #7f7f7f;
    font-size: 10px;
  }

  .clickItem-icon-share:hover + .clickItem-title-share {
    /* color: #53b681; */
    cursor: pointer;
  }

  .clickItem-like {
    display: inline-block;
    text-align: center;
    padding: 2px;
  }

  .clickItem-icon-like {
    font-size: 12px;
    color: #333;
    background-color: #c2bfbf;
    padding: 5px;
    border-radius: 30px;
  }

  .clickItem-icon-like:hover {
    /* font-size: 10px; */
    /* color: #e53b7f; */
    /* background: #f5e4eb; */
    cursor: pointer;
  }

  .clickItem-title-like {
    font-family: inherit;
    margin-top: 4px;
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

iframe {
  width: 100%;
  max-width: 650px; /* Also helpful. Optional. */
}
</style>
