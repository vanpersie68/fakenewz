<template>
  <div class="options">
    <h1 class="close-header">{{ $t('pOptionsArticles.socialPostFormat') }}</h1>
    <dropdown-base :options="[
      'Twitter',
      'Facebook',
      'Youtube',
      'TikTok',
      'Instagram',
      'Reddit',
      'Linkedin',
      'Tumblr',
      'Pinterest',
      'Quora',
      'Mastodon',
      'Mix',
    ]" :icons="[
  'x-twitter',
  'fab fa-facebook',
  'fab fa-youtube',
  'fab fa-tiktok',
  'fab fa-instagram',
  'fab fa-reddit',
  'fab fa-linkedin',
  'fab fa-tumblr',
  'fab fa-pinterest',
  'fab fa-quora',
  'fab fa-mastodon',
  'fab fa-mix',
]" :currentType="question.articleStyle" @input="handlePostStyle" class="secondary-drop" />
    <line-base class="dark" />

    <h1>{{ $t('pOptionsArticles.socialEngagement') }}</h1>
    <line-base class="light" />

    <div v-if="question.articleStyle === 'Linkedin'">
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.likeCount') }}</h2>
        <toggle-base :toggled="question.articleLikesOn" @handleToggle="activateLikeCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.commentCount') }}</h2>
        <toggle-base :toggled="question.articleCommentsOn" @handleToggle="activateCommentCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.repostCount') }}</h2>
        <toggle-base :toggled="question.articleRetweetsOn" @handleToggle="activateRetweetCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.sendCount') }}</h2>
        <toggle-base :toggled="question.articleSendsOn" @handleToggle="activateSendCount"></toggle-base>
      </div>
    </div>

    <!--   <div v-if="question.articleStyle === 'Quora'">
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.upvote') }}</h2>
        <toggle-base
          :toggled="question.articleLikesOn"
          @handleToggle="activateLikeCount"
        ></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.commentCount') }}</h2>
        <toggle-base
          :toggled="question.articleCommentsOn"
          @handleToggle="activateCommentCount"
        ></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.repostCount') }}</h2>
        <toggle-base
          :toggled="question.articleRetweetsOn"
          @handleToggle="activateRetweetCount"
        ></toggle-base>
      </div>
    </div> -->

    <div v-else-if="question.articleStyle === 'Tumblr'">
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.likeCount') }}</h2>
        <toggle-base :toggled="question.articleLikesOn" @handleToggle="activateLikeCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.reblogCount') }}</h2>
        <toggle-base :toggled="question.articleRetweetsOn" @handleToggle="activateRetweetCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.shareCount') }}</h2>
        <toggle-base :toggled="question.articleSharesOn" @handleToggle="activateShareCount"></toggle-base>
      </div>
    </div>

    <div v-else>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.likeCount') }}</h2>
        <toggle-base :toggled="question.articleLikesOn" @handleToggle="activateLikeCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.commentCount') }}</h2>
        <toggle-base :toggled="question.articleCommentsOn" @handleToggle="activateCommentCount"></toggle-base>
      </div>
      <div class="text-with-button">
        <h2>{{ $t('pOptionsArticles.shareCount') }}</h2>
        <toggle-base :toggled="question.articleSharesOn" @handleToggle="activateShareCount"></toggle-base>
      </div>
    </div>
    <!-- <div class="text-with-button">
      <h2>{{ $t('pOptionsArticles.likeCount') }}</h2>
      <toggle-base
        :toggled="question.articleLikesOn"
        @handleToggle="activateLikeCount"
      ></toggle-base>
    </div>
    <div class="text-with-button">
      <h2>{{ $t('pOptionsArticles.commentCount') }}</h2>
      <toggle-base
        :toggled="question.articleCommentsOn"
        @handleToggle="activateCommentCount"
      ></toggle-base>
    </div>
    <div class="text-with-button">
      <h2>{{ $t('pOptionsArticles.shareCount') }}</h2>
      <toggle-base
        :toggled="question.articleSharesOn"
        @handleToggle="activateShareCount"
      ></toggle-base>
    </div> -->

    <h1 class="close-header">{{ $t('pOptionsButtonRow.numAddon') }}</h1>
    <text-box-num :value="question.addon.length.toString()" @update="(value) =>
        $store.commit('updateAddonList', {
          question: question,
          value: value,
        })
      " :key="this.question.addon.length" @increment="insertNewElement($store)"
      @decrement="removeLastElement($store)" />
    <line-base class="dark" />
    <h1 class="close-header">Number of comment</h1>
    <text-box-num :value="question.comments ? question.comments.length.toString() : '0'" @update="(value) =>
        $store.commit('updateAddonList', {
          question: question,
          value: value,
        })
      " :key="question.comments ? question.comments.length.toString() : '0'" @increment="insertComment($store)"
      @decrement="removeLastComment($store)" />
    <line-base class="dark" />
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'
import TextBoxNum from './TextBoxNum.vue'
import DropdownBase from './DropdownBase.vue'
import LineBase from './LineBase.vue'
import ToggleBase from './ToggleBase.vue'
import store from '../../store/SurveyBuilder.js'

export default {
  name: 'PanelOptionsArticle',
  store: store,
  components: {
    ToggleBase,
    LineBase,
    TextBoxNum,
    DropdownBase,
  },
  props: {
    question: Object,
  },
  mounted() {
    console.log(this.question)
  },
  methods: {
    insertComment() {
      if (this.question.comments.length >= 5) {
        this.$message.warning('five comments max')
        return
      }
      SurveyServices.postComment(this.question.question, {
        content: '',
        username: '',
      }).then((res) => {
        this.question.comments.push(res)
      })
    },
    removeLastComment() {
      if (!this.question.comments.length) return
      SurveyServices.delComment(
        this.question.comments[this.question.comments.length - 1].id
      )
      this.question.comments.pop()
    },
    /**
     * Change and save the post style of a news post question
     */
    async handlePostStyle(style) {
      store.commit('updateValue', {
        parent: this.question,
        key: 'articleStyle',
        value: style,
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleStyle: style,
      })
    },
    /**
     * Toggle and save whether to have like count or not
     */
    async activateLikeCount() {
      store.commit('toggle', { parent: this.question, key: 'articleLikesOn' })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleLikesOn: this.question.articleLikesOn,
      })
    },
    /**
     * Toggle and save whether to have comment count or not
     */
    async activateCommentCount() {
      store.commit('toggle', {
        parent: this.question,
        key: 'articleCommentsOn',
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleCommentsOn: this.question.articleCommentsOn,
      })
    },
    /**
     * Toggle and save whether to have share count or not
     */
    async activateShareCount() {
      store.commit('toggle', { parent: this.question, key: 'articleSharesOn' })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleSharesOn: this.question.articleSharesOn,
      })
    },
    async activateRetweetCount() {
      store.commit('toggle', {
        parent: this.question,
        key: 'articleRetweetsOn',
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleRetweetsOn: this.question.articleRetweetsOn,
      })
    },
    async activateSendCount() {
      store.commit('toggle', { parent: this.question, key: 'articleSendsOn' })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleSendsOn: this.question.articleSendsOn,
      })
    },
    async insertNewElement(store) {
      console.log(this.question.addon.length)
      if (this.question.addon.length < 2) {
        const resp = await SurveyServices.postPostAddonfield(
          this.question.typedata.id,
          {
            tittle: this.$t('app.buttonDefault'),
          }
        )

        store.commit('insertLastElement', {
          list: this.question.addon,
          element: { tittle: this.$t('app.buttonDefault'), ...resp },
        })

        console.log(this.question.addon, resp)
        // vm.$forceUpdate();
        // this.question.buttons = this.question.buttons
      } else {
        await this.$alert(
          'Maximum number of additional field must less than 2',
          'Warning',
          {
            confirmButtonText: 'Confirm',
          }
        )
      }
    },
    /**
     * Remove last button from button row and save
     */
    async removeLastElement(store) {
      const temp_id = this.question.addon.slice(-1)[0].id
      store.commit('removeLastElement', this.question.addon)

      await SurveyServices.deletepostPostAddonfield(this.question.typedata.id, {
        id: String(temp_id),
      })
    },
  },
}
</script>

<style scoped>
html:lang(ur) * {
  text-align: right;
}

h1,
h2 {
  color: black;
  padding: 0 16px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  text-align: left;
}

h1 {
  font-size: 16px;
  font-weight: bold;
  padding: 16px;
}

h2 {
  font-size: 16px;
  font-weight: bold;
}

.close-header {
  padding-bottom: 0px;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-content: center;
}

.secondary-drop {
  z-index: 9;
}
</style>
