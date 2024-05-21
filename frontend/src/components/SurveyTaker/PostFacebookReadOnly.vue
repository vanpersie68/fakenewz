<template>
  <div class="post">
    <a :href="question.articleURL" target="_blank" v-if="isImage"
      ><img
        :src="question.articleImage"
        :alt="question.articleTitle"
        width="100%"
        height="auto"
    /></a>
    <div v-else class="no-image">{{ $t('postEditable.noImage') }}</div>
    <p>
      {{ question.articleSource.toUpperCase() }}
    </p>
    <h1>
      <a
        :href="question.articleURL"
        style="text-decoration: none; color: black"
        target="_blank"
        >{{ question.articleTitle }}</a
      >
    </h1>
    <LineBase class="line-base" />

    <div v-show="mode1Show">
      <el-row class="count-row">
        <el-col class="count-col" :span="2" v-show="likeShow">
          <el-image
            class="like-img"
            src="data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 16 16'%3e%3cdefs%3e%3clinearGradient id='a' x1='50%25' x2='50%25' y1='0%25' y2='100%25'%3e%3cstop offset='0%25' stop-color='%2318AFFF'/%3e%3cstop offset='100%25' stop-color='%230062DF'/%3e%3c/linearGradient%3e%3cfilter id='c' width='118.8%25' height='118.8%25' x='-9.4%25' y='-9.4%25' filterUnits='objectBoundingBox'%3e%3cfeGaussianBlur in='SourceAlpha' result='shadowBlurInner1' stdDeviation='1'/%3e%3cfeOffset dy='-1' in='shadowBlurInner1' result='shadowOffsetInner1'/%3e%3cfeComposite in='shadowOffsetInner1' in2='SourceAlpha' k2='-1' k3='1' operator='arithmetic' result='shadowInnerInner1'/%3e%3cfeColorMatrix in='shadowInnerInner1' values='0 0 0 0 0 0 0 0 0 0.299356041 0 0 0 0 0.681187726 0 0 0 0.3495684 0'/%3e%3c/filter%3e%3cpath id='b' d='M8 0a8 8 0 00-8 8 8 8 0 1016 0 8 8 0 00-8-8z'/%3e%3c/defs%3e%3cg fill='none'%3e%3cuse fill='url(%23a)' xlink:href='%23b'/%3e%3cuse fill='black' filter='url(%23c)' xlink:href='%23b'/%3e%3cpath fill='white' d='M12.162 7.338c.176.123.338.245.338.674 0 .43-.229.604-.474.725a.73.73 0 01.089.546c-.077.344-.392.611-.672.69.121.194.159.385.015.62-.185.295-.346.407-1.058.407H7.5c-.988 0-1.5-.546-1.5-1V7.665c0-1.23 1.467-2.275 1.467-3.13L7.361 3.47c-.005-.065.008-.224.058-.27.08-.079.301-.2.635-.2.218 0 .363.041.534.123.581.277.732.978.732 1.542 0 .271-.414 1.083-.47 1.364 0 0 .867-.192 1.879-.199 1.061-.006 1.749.19 1.749.842 0 .261-.219.523-.316.666zM3.6 7h.8a.6.6 0 01.6.6v3.8a.6.6 0 01-.6.6h-.8a.6.6 0 01-.6-.6V7.6a.6.6 0 01.6-.6z'/%3e%3c/g%3e%3c/svg%3e"
            v-show="likeShow"
            ><span>&nbsp</span></el-image
          >
        </el-col>

        <el-col :span="6">
          <span v-show="likeShow">{{ question.articleLikes }} likes</span>
        </el-col>

        <el-col span="15" style="text-align: right">
          <span>{{ countLine }}</span>
        </el-col>
      </el-row>
      <LineBase class="line-base" />

      <el-row class="btn-row">
        <el-col style="text-align: center" :style="colWidth" v-show="likeShow">
          <button
            class="click-button"
            @click="clickItem('Like')"
            :style="likeColor"
          >
            <span class="iconfont click-icon">&#xe7c8;</span> Like
          </button>
        </el-col>
        <el-col
          :style="colWidth"
          style="text-align: center"
          v-show="commentShow"
        >
          <button
            class="click-button"
            @click="clickItem('Comment')"
            :style="commentColor"
          >
            <span class="iconfont click-icon">&#xe651;</span> Comment
          </button>
        </el-col>
        <el-col :style="colWidth" style="text-align: center" v-show="shareShow">
          <button
            class="click-button"
            @click="clickItem('Share')"
            :style="shareColor"
          >
            <span class="iconfont click-icon">&#xe6ef;</span> Share
          </button>
        </el-col>
        <el-col
          :style="colWidth"
          style="text-align: center"
          v-show="addon1Show"
        >
          <button
            class="click-button"
            @click="clickItem('Add1')"
            :style="add1Color"
          >
            <i :class="add1Icon" class="click-icon"></i> {{ add1Title }}
          </button>
        </el-col>
        <el-col
          :style="colWidth"
          style="text-align: center"
          v-show="addon2Show"
        >
          <button
            class="click-button"
            @click="clickItem('Add2')"
            :style="add2Color"
          >
            <i :class="add2Icon" class="click-icon"></i> {{ add2Title }}
          </button>
        </el-col>
      </el-row>
      <LineBase class="line-base" />
    </div>

    <div v-show="mode2Show">
      <el-row class="count-row">
        <el-col class="count-col" :span="2" v-show="likeShow">
          <el-image
            class="like-img"
            src="data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 16 16'%3e%3cdefs%3e%3clinearGradient id='a' x1='50%25' x2='50%25' y1='0%25' y2='100%25'%3e%3cstop offset='0%25' stop-color='%2318AFFF'/%3e%3cstop offset='100%25' stop-color='%230062DF'/%3e%3c/linearGradient%3e%3cfilter id='c' width='118.8%25' height='118.8%25' x='-9.4%25' y='-9.4%25' filterUnits='objectBoundingBox'%3e%3cfeGaussianBlur in='SourceAlpha' result='shadowBlurInner1' stdDeviation='1'/%3e%3cfeOffset dy='-1' in='shadowBlurInner1' result='shadowOffsetInner1'/%3e%3cfeComposite in='shadowOffsetInner1' in2='SourceAlpha' k2='-1' k3='1' operator='arithmetic' result='shadowInnerInner1'/%3e%3cfeColorMatrix in='shadowInnerInner1' values='0 0 0 0 0 0 0 0 0 0.299356041 0 0 0 0 0.681187726 0 0 0 0.3495684 0'/%3e%3c/filter%3e%3cpath id='b' d='M8 0a8 8 0 00-8 8 8 8 0 1016 0 8 8 0 00-8-8z'/%3e%3c/defs%3e%3cg fill='none'%3e%3cuse fill='url(%23a)' xlink:href='%23b'/%3e%3cuse fill='black' filter='url(%23c)' xlink:href='%23b'/%3e%3cpath fill='white' d='M12.162 7.338c.176.123.338.245.338.674 0 .43-.229.604-.474.725a.73.73 0 01.089.546c-.077.344-.392.611-.672.69.121.194.159.385.015.62-.185.295-.346.407-1.058.407H7.5c-.988 0-1.5-.546-1.5-1V7.665c0-1.23 1.467-2.275 1.467-3.13L7.361 3.47c-.005-.065.008-.224.058-.27.08-.079.301-.2.635-.2.218 0 .363.041.534.123.581.277.732.978.732 1.542 0 .271-.414 1.083-.47 1.364 0 0 .867-.192 1.879-.199 1.061-.006 1.749.19 1.749.842 0 .261-.219.523-.316.666zM3.6 7h.8a.6.6 0 01.6.6v3.8a.6.6 0 01-.6.6h-.8a.6.6 0 01-.6-.6V7.6a.6.6 0 01.6-.6z'/%3e%3c/g%3e%3c/svg%3e"
            v-show="likeShow"
            ><span>&nbsp</span></el-image
          >
        </el-col>

        <el-col :span="6">
          <span v-show="likeShow">{{ question.articleLikes }} likes</span>
        </el-col>

        <el-col span="15" style="text-align: right">
          <span>{{ countLine }}</span>
        </el-col>
      </el-row>
      <LineBase class="line-base" />

      <el-row class="btn-row">
        <el-col style="text-align: center" :style="colWidth" v-show="likeShow">
          <button
            class="click-button"
            @click="clickItem('Like')"
            :style="likeColor"
          >
            <span class="iconfont click-icon">&#xe7c8;</span> Like
          </button>
        </el-col>
        <el-col
          :style="colWidth"
          style="text-align: center"
          v-show="commentShow"
        >
          <button
            class="click-button"
            @click="clickItem('Comment')"
            :style="commentColor"
          >
            <span class="test iconfont click-icon">&#xe651;</span> Comment
          </button>
        </el-col>
        <el-col :style="colWidth" style="text-align: center" v-show="shareShow">
          <button
            class="click-button"
            @click="clickItem('Share')"
            :style="shareColor"
          >
            <span class="iconfont click-icon">&#xe6ef;</span> Share
          </button>
        </el-col>
      </el-row>
      <LineBase class="line-base" />

      <el-row class="btn-row">
        <el-col
          :style="newColWidth"
          style="text-align: center"
          v-show="addon1Show"
        >
          <button
            class="click-button"
            @click="clickItem('Add1')"
            :style="add1Color"
          >
            <i :class="add1Icon" class="click-icon"></i> {{ add1Title }}
          </button>
        </el-col>
        <el-col
          :style="newColWidth"
          style="text-align: center"
          v-show="addon2Show"
        >
          <button
            class="click-button"
            @click="clickItem('Add2')"
            :style="add2Color"
          >
            <i :class="add2Icon" class="click-icon"></i> {{ add2Title }}
          </button>
        </el-col>
      </el-row>
      <LineBase class="line-base" />
    </div>

    <span class="tip-box" v-if="questionData.required === true">
      <span style="color: red">{{ $t('surveyTaker.tips') }}</span>
      {{ $t('surveyTaker.tipHint') }}
    </span>
  </div>
</template>

<script>
import store from '../../store/SurveyBuilder.js'
import LineBase from '@/components/SurveyBuilder/LineBase'

export default {
  name: 'PostFacebookReadOnly',
  store: store,
  props: {
    question: Object,
  },
  components: {
    LineBase,
  },
  data() {
    return {
      questionData: '',

      countItems: 0,
      clickItems: [],
      countLine: '',

      likeShow: false,
      commentShow: false,
      shareShow: false,
      addon1Show: false,
      addon2Show: false,
      additionalFieldShow: false,
      mode1Show: false,
      mode2Show: false,

      likeFlag: false,
      commentFlag: false,
      shareFlag: false,
      add1Flag: false,
      add2Flag: false,

      add1Title: '',
      add1Icon: '',
      add1Count: '',

      add2Title: '',
      add2Icon: '',
      add2Count: '',

      likeColor: '',
      commentColor: '',
      shareColor: '',
      add1Color: '',
      add2Color: '',

      colWidth: '',
      newColWidth: '',

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
    this.addClickItems()
    this.selectMode()
    this.checkShow()
    this.initializeAnswer()
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

    openCommentDialog() {
      this.$prompt('Write a comment', 'Comment', {
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
            if (this.answerObj[i].title === 'Comment') {
              this.answerObj[i].answerText = value
            }
          }
          this.sendResult()
          this.updateCount()
          this.$message({
            type: 'success',
            message: 'Success comment',
          })
        })
        .catch(() => {
          this.cancelCheckComment()
          this.changeCommentColor(false)
          this.question.articleComments--
          this.commentFlag = false
          this.$message({
            type: 'info',
            message: 'Cancel',
          })
        })
    },

    cancelCheckComment() {
      for (let i = 0; i < this.countItems; i++) {
        if (this.answerObj[i].title === 'Comment') {
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
      this.$prompt('Please input something', this.questionData.addon[0].title, {
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
          this.updateCount()
          this.sendResult()
          this.$message({
            type: 'success',
            message: 'Success',
          })
        })
        .catch(() => {
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
        if (this.answerObj[i].title === this.add1Title) {
          this.answerObj[i].answerText = ''
        }
      }
    },

    openAdd2Dialog() {
      this.$prompt('Please input something', this.questionData.addon[1].title, {
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
          this.updateCount()
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

    changeLikeColor(flag) {
      if (flag === true) {
        this.likeColor = 'color: #3573E0'
      } else {
        this.likeColor = 'color: #050505'
      }
    },

    changeCommentColor(flag) {
      if (flag === true) {
        this.commentColor = 'color: #3573E0'
      } else {
        this.commentColor = 'color: #050505'
      }
    },

    changeShareColor(flag) {
      if (flag === true) {
        this.shareColor = 'color: #3573E0'
      } else {
        this.shareColor = 'color: #050505'
      }
    },

    changeAdd1Color(flag) {
      if (flag === true) {
        this.add1Color = 'color: #3573E0'
      } else {
        this.add1Color = 'color: #050505'
      }
    },

    changeAdd2Color(flag) {
      if (flag === true) {
        this.add2Color = 'color: #3573E0'
      } else {
        this.add2Color = 'color: #050505'
      }
    },

    clickItem(item) {
      if (item === 'Like') {
        this.likeFlag = !this.likeFlag
        if (this.likeFlag == true) {
          this.question.articleLikes++
          this.changeLikeColor(true)
          this.checkLike()
          this.sendResult()
        } else {
          this.question.articleLikes--
          this.changeLikeColor(false)
          this.cancelCheckLike()
          this.sendResult()
        }
      }
      if (item === 'Comment') {
        this.commentFlag = !this.commentFlag
        if (this.commentFlag == true) {
          this.question.articleComments++
          this.changeCommentColor(true)
          this.openCommentDialog()
        } else {
          this.question.articleComments--
          this.changeCommentColor(false)
          this.cancelCheckComment()
          this.sendResult()
          this.updateCount()
        }
      }
      if (item === 'Share') {
        this.shareFlag = !this.shareFlag
        if (this.shareFlag == true) {
          this.question.articleShares++
          this.changeShareColor(true)
          this.checkShare()
          this.sendResult()
          this.updateCount()
        } else {
          this.question.articleShares--
          this.changeShareColor(false)
          this.cancelCheckShare()
          this.sendResult()
          this.updateCount()
        }
      }

      if (item === 'Add1') {
        this.add1Flag = !this.add1Flag
        if (this.add1Flag == true) {
          this.add1Count++
          this.changeAdd1Color(true)
          this.openAdd1Dialog()
        } else {
          this.add1Count--
          this.changeAdd1Color(false)
          this.cancelCheckAdd1()
          this.sendResult()
          this.updateCount()
        }
      }
      if (item === 'Add2') {
        this.add2Flag = !this.add2Flag
        if (this.add2Flag == true) {
          this.add2Count++
          this.changeAdd2Color(true)
          this.openAdd2Dialog()
        } else {
          this.add2Count--
          this.changeAdd2Color(false)
          this.cancelCheckAdd2()
          this.sendResult()
          this.updateCount()
        }
      }
    },

    addClickItems() {
      let normalColsCount = 0
      if (this.questionData.articleCommentsOn === true) {
        this.clickItems.push('Comment')
        this.countItems++
        normalColsCount++
      }
      if (this.questionData.articleSharesOn === true) {
        this.clickItems.push('Share')
        this.countItems++
        normalColsCount++
      }
      if (this.questionData.articleLikesOn === true) {
        this.clickItems.push('Like')
        this.countItems++
        normalColsCount++
      }

      if (this.questionData.addon.length != 0) {
        for (let i = 0; i < this.questionData.addon.length; i++) {
          this.clickItems.push(this.questionData.addon[i].title)
        }
        this.countItems = this.countItems + this.questionData.addon.length
      }

      if (normalColsCount == 1) {
        this.colWidth = 'width: 100%'
      }
      if (normalColsCount == 2) {
        this.colWidth = 'width: 50%'
      }
      if (normalColsCount == 3) {
        this.colWidth = 'width: 33.3%'
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
        this.newColWidth = 'width: 33.3%'
      }
      if (this.countItems == 5) {
        this.newColWidth = 'width: 33.3%'
      }
    },

    checkShow() {
      this.commentShow = this.questionData.articleCommentsOn
      this.shareShow = this.questionData.articleSharesOn
      this.likeShow = this.questionData.articleLikesOn
      if (this.questionData.addon.length > 0) {
        this.additionalFieldShow = true
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
      }
      this.getCount()
    },

    getCount() {
      if (this.questionData.articleCommentsOn === true) {
        this.countLine =
          this.countLine + this.questionData.articleComments + ' comments '
      }
      if (this.questionData.articleSharesOn === true) {
        this.countLine =
          this.countLine + this.questionData.articleShares + ' shares '
      }

      if (this.questionData.addon.length === 1) {
        this.countLine =
          this.countLine +
          this.add1Count +
          ' ' +
          this.questionData.addon[0].title +
          's '
      }
      if (this.questionData.addon.length === 2) {
        this.countLine =
          this.countLine +
          this.add1Count +
          ' ' +
          this.questionData.addon[0].title +
          's '
        this.countLine =
          this.countLine +
          this.add2Count +
          ' ' +
          this.questionData.addon[1].title +
          's '
      }
    },

    updateCount() {
      this.countLine = ''
      if (this.questionData.articleCommentsOn === true) {
        this.countLine =
          this.countLine + this.questionData.articleComments + ' comments '
      }
      if (this.questionData.articleSharesOn === true) {
        this.countLine =
          this.countLine + this.questionData.articleShares + ' shares '
      }

      if (this.questionData.addon.length === 1) {
        this.countLine =
          this.countLine +
          this.add1Count +
          ' ' +
          this.questionData.addon[0].title +
          's '
      }
      if (this.questionData.addon.length === 2) {
        this.countLine =
          this.countLine +
          this.add1Count +
          ' ' +
          this.questionData.addon[0].title +
          's '
        this.countLine =
          this.countLine +
          this.add2Count +
          ' ' +
          this.questionData.addon[1].title +
          's '
      }
    },

    selectMode() {
      if (this.countItems === 0) {
        this.mode1Show = false
        this.mode2Show = false
      } else if (0 < this.countItems <= 3) {
        this.mode1Show = true
      } else {
        this.mode2Show = true
      }
    },
  },

  computed: {
    /**
     * Check whether it is an image or not
     * @returns {boolean} false if not an image and true otherwise
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

.post {
  border: 1px solid #f0f2f5;
  width: 88%;
  background-color: white;
  margin: 0 auto;
  margin-top: 30px;
  padding-bottom: 10px;
}

.no-image {
  background-color: #d1d9dd;
  height: 100px;
  width: 100%;
  color: black;
  text-align: center;
}

.click-button:hover {
  background: #f2f2f2;
  color: #606266;
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

@media (min-width: 1130px) {
  .tip-box {
    font-size: 13px;
    color: #6e6e6e;
    margin: 8px;
    padding: 8px;
  }

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 13px;
    line-height: 15px;
    text-align: left;
    color: #65676b;
    margin: 6px 16px;
  }
  h1 {
    font-family: Arial;
    font-style: normal;
    font-weight: bold;
    font-size: 17px;
    line-height: 20px;
    text-align: left;
    margin: 0 16px;
    color: #050505;
  }

  .click-button {
    width: 95%;
    height: 30px;
    border: white;
    background: white;
    border-radius: 2px;
    font-size: 15px;
  }
  .btn-row {
    margin-left: 17px;
    margin-right: 17px;
  }

  .line-base {
    color: #dbdddf;
    margin-right: 3%;
    margin-left: 3%;
    width: 94%;
  }

  .like-img {
    width: 22px;
    height: 22px;
    margin-right: 10px;
  }
  .count-row {
    font-size: 14px;
    color: #6e6e6e;
  }
  .count-col {
    padding-left: 20px;
  }
}

@media (max-width: 1129px) and (min-width: 890px) {
  .tip-box {
    font-size: 9px;
    color: #6e6e6e;
    margin: 6px;
    padding: 6px;
  }

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 13px;
    line-height: 15px;
    text-align: left;
    color: #65676b;
    margin: 6px 16px;
  }
  h1 {
    font-family: Arial;
    font-style: normal;
    font-weight: bold;
    font-size: 17px;
    line-height: 20px;
    text-align: left;
    margin: 0 16px;
    color: #050505;
  }

  .click-button {
    width: 95%;
    height: 30px;
    border: white;
    background: white;
    border-radius: 2px;
  }
  .btn-row {
    margin-left: 20px;
    margin-right: 20px;
  }

  .line-base {
    color: #dbdddf;
    margin-right: 3%;
    margin-left: 3%;
    width: 94%;
  }

  .like-img {
    width: 22px;
    height: 22px;
    margin-right: 10px;
  }
  .count-row {
    font-size: 13px;
    color: #6e6e6e;
  }
  .count-col {
    padding-left: 20px;
  }
}

@media (max-width: 889px) {
  .post {
    margin-top: 0px;
    margin-bottom: 10px;
    width: 96%;
  }
  .tip-box {
    font-size: 10px;
    color: #6e6e6e;
    margin: 2px 8px 2px 8px;
    padding: 4px;
  }

  p {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 4px;
    line-height: 6px;
    text-align: left;
    color: #65676b;
    margin: 4px 10px;
  }

  h1 {
    font-family: Helvetica, Arial, sans-serif;
    font-style: normal;
    font-weight: bold;
    font-size: 14px;
    line-height: 16px;
    text-align: left;
    margin: 0 10px;
    color: #050505;
  }

  .click-button {
    width: 100%;
    height: 25px;
    border: white;
    background: white;
    border-radius: 2px;
    margin: 0px;
    padding: 0px;
  }

  .btn-row {
    margin-left: 8px;
    margin-right: 8px;
  }

  .click-icon {
    font-size: 10px;
  }

  .line-base {
    color: #dbdddf;
    margin-right: 3%;
    margin-left: 3%;
    width: 94%;
  }
  .like-img {
    width: 15px;
    height: 15px;
  }

  .count-row {
    font-size: 10px;
    color: #6e6e6e;
  }

  .count-col {
    padding-left: 13px;
  }
}
</style>
