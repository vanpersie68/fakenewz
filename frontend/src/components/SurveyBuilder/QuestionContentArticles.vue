<template>
  <div>
    <h3 v-if="$i18n.locale === 'ur' &&
      content.articleStyle !== 'Youtube' &&
      content.articleStyle !== 'TikTok'
      " style="text-align: right; margin-bottom: 0">
      {{ $t('qContentArticles.articleLink') }}
    </h3>
    <h3 v-else-if="$i18n.locale !== 'ur' &&
      content.articleStyle !== 'Youtube' &&
      content.articleStyle !== 'TikTok'
      " style="text-align: left; margin-bottom: 0">
      {{ $t('qContentArticles.articleLink') }}
    </h3>
    <h3 v-else-if="$i18n.locale === 'ur' && content.articleStyle === 'Youtube'"
      style="text-align: right; margin-bottom: 0">
      {{ $t('qContentArticles.videoLink') }}
    </h3>
    <h3 v-else-if="$i18n.locale === 'ur' && content.articleStyle === 'TikTok'"
      style="text-align: right; margin-bottom: 0">
      {{ $t('qContentArticles.videoLink') }}
    </h3>
    <h3 v-else style="text-align: left; margin-bottom: 0">
      {{ $t('qContentArticles.videoLink') }}
    </h3>
    <div class="text-with-button">
      <input type="text" v-model="articleURL" style="width: 100%" @unfocus="(value) => (articleURL = value)" v-if="content.articleStyle !== 'Youtube' &&
        content.articleStyle !== 'TikTok'
        " :placeholder="$t('qContentArticles.articleLinkPlaceholder')" />
      <input type="text" v-model="articleURL" style="width: 100%" @unfocus="(value) => (articleURL = value)" v-else
        :placeholder="$t('qContentArticles.videoLinkPlaceholder')" />

      <button-base class="primary standard" :title="$t('qContentArticles.fetch')" v-if="content.articleStyle !== 'Youtube' &&
        content.articleStyle !== 'TikTok'
        " @buttonPress="fetchData" />

      <button-base class="primary standard" :title="$t('qContentArticles.fetch')" v-else @buttonPress="fetchVideoData" />
    </div>

    <line-base class="light" />

    <label v-if="content.articleStyle !== 'Youtube' && content.articleStyle !== 'TikTok'
      " for="imageURL">{{ $t('qContentArticles.imageLink') }}</label>
    <div v-if="content.articleStyle !== 'Youtube' && content.articleStyle !== 'TikTok'
      " class="text-with-button">
      <input type="text" id="imageURL" name="imageURL" :placeholder="$t('qContentArticles.imageLinkPlaceholder')"
        v-model="imageURL" @input="updateImage" />
      <button-base class="primary standard" :title="$t('qContentArticles.refresh')" @buttonPress="refreshImage" />
    </div>

    <line-base class="light" />

    <h3 v-if="content.articleStyle !== 'Youtube' && content.articleStyle !== 'TikTok'
      ">
      {{ $t('qContentArticles.editablePreview') }}
    </h3>

    <post-twitter-editable v-if="content.articleStyle === 'Twitter'" :question="data" />

    <post-facebook-editable v-else-if="content.articleStyle === 'Facebook'" :question="data" />
    <post-instagram-editable v-else-if="content.articleStyle === 'Instagram'" :question="data" />
    <post-reddit-editable v-else-if="content.articleStyle === 'Reddit'" :question="data" />

    <post-youtube-editable v-else-if="content.articleStyle === 'Youtube'" :question="data" />
    <post-tik-tok-editable v-else-if="content.articleStyle === 'TikTok'" :question="data" />
    <post-linkedin-editable v-else-if="content.articleStyle === 'Linkedin'" :question="data" />

    <post-tumblr-editable v-else-if="content.articleStyle === 'Tumblr'" :question="data" />

    <post-pinterest-editable v-else-if="content.articleStyle === 'Pinterest'" :question="data" />

    <post-quora-editable v-else-if="content.articleStyle === 'Quora'" :question="data" />

    <post-mastodon-editable v-else-if="content.articleStyle === 'Mastodon'" :question="data" />

    <post-mix-editable v-else-if="content.articleStyle === 'Mix'" :question="data" />

    <div v-if="content.articleLikesOn">
      <line-base class="light" />
      <label for="likeCount">{{ $t('qContentArticles.likeCount') }}</label>
      <input type="text" id="likeCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="likeCount" :placeholder="$t('qContentArticles.likePlaceholder')" v-model="likeCount" @input="updateLikes" />
    </div>

    <div v-if="content.articleCommentsOn && content.articleStyle !== 'Tumblr'">
      <line-base class="light" />
      <label for="commentCount">{{
        $t('qContentArticles.commentCount')
      }}</label>
      <input type="text" id="commentCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="commentCount" :placeholder="$t('qContentArticles.commentPlaceholder')" v-model="commentCount"
        @input="updateComments" />
    </div>

    <div v-if="data.articleRetweetsOn && content.articleStyle == 'Tumblr'">
      <line-base class="light" />
      <label for="retweetCount">{{ $t('qContentArticles.reblogCount') }}</label>
      <input type="text" id="retweetCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="retweetCount" :placeholder="$t('qContentArticles.reblogPlaceholder')" v-model="retweetCount"
        @input="updateRetweets" />
    </div>

    <div v-if="data.articleSharesOn && content.articleStyle !== 'Linkedin'">
      <line-base class="light" />
      <label for="shareCount">{{ $t('qContentArticles.shareCount') }}</label>
      <input type="text" id="shareCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="shareCount" :placeholder="$t('qContentArticles.sharePlaceholder')" v-model="shareCount"
        @input="updateShares" />
    </div>

    <div v-if="data.articleRetweetsOn && content.articleStyle == 'Linkedin'">
      <line-base class="light" />
      <label for="retweetCount">{{ $t('qContentArticles.repostCount') }}</label>
      <input type="text" id="retweetCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="retweetCount" :placeholder="$t('qContentArticles.repostPlaceholder')" v-model="retweetCount"
        @input="updateRetweets" />
    </div>

    <div v-if="data.articleSendsOn && content.articleStyle == 'Linkedin'">
      <line-base class="light" />
      <label for="sendCount">{{ $t('qContentArticles.sendCount') }}</label>
      <input type="text" id="sendCount" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
        name="sendCount" :placeholder="$t('qContentArticles.sendPlaceholder')" v-model="sendCount" @input="updateSends" />
    </div>

    <div v-if="data.addon.length > 0">
      <line-base class="light" />

      <h2 style="font-weight: 700; font-size: 16px">
        {{ $t('builderQuestion.addonContent') }}
      </h2>
      <div v-for="ad in data.addon" :key="data.addon.indexOf(ad)" class="question-titles">
        <h1 style="
            font-weight: 500;
            font-size: 20px;
            padding-right: 5px;
            font-family: Menlo;
          ">
          {{ data.addon.indexOf(ad) + 1 }}.
        </h1>

        <!--add icon-->
        <SelectIcons @selected="getData" style="width: 35%" :index="data.addon.indexOf(ad)" :iconShow="ad.icon">
        </SelectIcons>

        &nbsp&nbsp
        <!--add title-->
        <el-input type="text" maxlength="8" placeholder="Title" v-model="data.addon[data.addon.indexOf(ad)].title"
          @blur="(input) => inputAddon(data.addon[data.addon.indexOf(ad)])" />

        &nbsp&nbsp
        <!--add count-->
        <el-input type="text" placeholder="Count" onKeypress="return (/[\d]/.test(String.fromCharCode(event.keyCode)))"
          v-model="data.addon[data.addon.indexOf(ad)].count"
          @blur="(input) => inputAddon(data.addon[data.addon.indexOf(ad)])" />
      </div>
    </div>
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'

import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import PostFacebookEditable from './PostFacebookEditable.vue'
import PostTwitterEditable from './PostTwitterEditable.vue'
import PostYoutubeEditable from './PostYoutubeEditable.vue'
import PostTikTokEditable from './PostTikTokEditable.vue'
import PostInstagramEditable from './PostInstagramEditable.vue'
import PostRedditEditable from './PostRedditEditable.vue'
import PostLinkedinEditable from './PostLinkedinEditable.vue'
import PostTumblrEditable from './PostTumblrEditable.vue'
import PostPinterestEditable from './PostPinterestEditable.vue'
import PostMixEditable from './PostMixEditable.vue'

import store from '../../store/SurveyBuilder.js'
import TextBox from './TextBox.vue'
import SelectIcons from '@/components/SurveyBuilder/SelectIcons'
import PostQuoraEditable from "@/components/SurveyBuilder/PostQuoraEditable.vue";
import PostMastodonEditable from "@/components/SurveyBuilder/PostMastodonEditable.vue";

export default {
  name: 'QuestionContentArticles',
  store: store,
  components: {
    PostMastodonEditable,
    PostQuoraEditable,
    PostTwitterEditable,
    PostFacebookEditable,
    PostYoutubeEditable,
    PostTikTokEditable,
    PostInstagramEditable,
    PostRedditEditable,
    PostLinkedinEditable,
    PostTumblrEditable,
    PostPinterestEditable,
    PostMastodonEditable,
    PostQuoraEditable,
    PostMixEditable,
    LineBase,
    ButtonBase,
    TextBox,
    SelectIcons,
  },
  props: {
    data: Object,
  },
  data() {
    return {
      articleURL: this.data.articleURL,
      imageURL: this.data.articleImage,
      likeCount: this.data.likeCount,
      commentCount: this.data.commentCount,
      shareCount: this.data.shareCount,
      retweetCount: this.data.retweetCount,
      sendCount: this.data.sendCount,
      content: this.data,
    }
  },
  methods: {
    getData(name, index) {
      this.data.addon[index].icon = name
      this.inputAddon(this.data.addon[index])
    },

    /**
     * Update image inside news post question
     * @param e - event
     */
    updateImage(e) {
      this.imageURL = e.target.value
    },
    /**
     * Handle and save refreshed image upon refresh button being pressed
     */
    async refreshImage() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articleImage',
        value: this.imageURL,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleImageLink: this.imageURL,
      })
    },
    /**
     * Fetch and populate metadata for news post question after link provided
     */
    async fetchData() {
      const response = await SurveyServices.getLinkInformation({
        link: this.articleURL,
      })

      store.dispatch('fetchData', {
        resp: response,
        resetValues: () => this.resetValues(),
        question: this.data,
      })

      this.imageURL = this.data.articleImage

      await SurveyServices.patchQuestionType(this.data.id, {
        articleImageLink: this.imageURL,
        articleURL: response.url,
        articleSource: response.urlShort,
        articleTitle: response.title,
        articleSnippet: response.description,
        articleStyle: this.content.articleStyle,
      })

      this.resetValues()
    },

    async fetchVideoData() {
      let response
      if (this.articleURL.includes('tiktok')) {
        // response = {
        //   embed_url: this.articleURL,
        //   video_title:'',
        //   video_id: this.articleURL.match(/video\/(\d+)/)[1],
        //   articleUser: this.articleURL.match(/\@[^\/]+/)[0],
        // }
        response = await SurveyServices.getVideoLinkInformation(this.articleURL)
      } else {
        response = await SurveyServices.getVideoLinkInformation(this.articleURL)
      }

      // this.tikData = response
      store.dispatch('fetchVideoData', {
        resp: response,
        question: this.data,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleImageLink: '',
        articleURL: response.embed_url,
        articleTitle: response.video_title,
        articleStyle: this.content.articleStyle,
        articleSource: response.video_id,
        articleUser: response.articleUser,
        articleImageLink: response.articleImageLink,
        articleSnippet: '',
      })
    },
    async updateComments() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articleComments',
        value: this.commentCount,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleComments: this.commentCount,
      })
    },
    /**
     * Handle and save like count being edited
     */
    async updateLikes() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articleLikes',
        value: this.likeCount,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleLikes: this.likeCount,
      })
    },
    /**
     * Handle and save share count being edited
     */
    async updateShares() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articleShares',
        value: this.shareCount,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleShares: this.shareCount,
      })
    },

    /**
     * Handle and save retweets count being edited
     */
    async updateRetweets() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articlesRetweets',
        value: this.retweetCount,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleRetweets: this.retweetCount,
      })
    },
    /**
     * Handle and save send count being edited
     */
    async updateSends() {
      store.commit('updateValue', {
        parent: this.data,
        key: 'articleSends',
        value: this.sendCount,
      })

      await SurveyServices.patchQuestionType(this.data.id, {
        articleSends: this.sendCount,
      })
    },

    /**
     * Reset the image url
     */
    resetValues() {
      this.imageURL = this.data.articleImage
    },
    async inputAddon(addon) {
      await SurveyServices.patchPostAddonfield(this.data.typedata.id, {
        id: addon.id,
        title: this.data.addon[this.data.addon.indexOf(addon)].title,
        count: this.data.addon[this.data.addon.indexOf(addon)].count,
        icon: this.data.addon[this.data.addon.indexOf(addon)].icon,
      })
    },
  },
}
</script>

<style scoped lang="scss">
@import './src/assets/textbox.scss';

html:lang(ur) * {
  text-align: right;
}

input[type='text'] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: 2px solid red;
  border-radius: 4px;
  padding: 8px;
  border: 2px solid #eff2f5;
}

h3,
label {
  color: black;
  padding: 0 0 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: bold;
  text-align: left;
  margin-right: 8px;
  font-size: 16px;
}

h3 {
  text-align: center;
}

label {
  display: block;
  text-align: left;
}

input {
  color: black;
  padding: 0 0 0 8px;
  font-family: Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: normal;
  text-align: left;
  margin-right: 8px;
  font-size: 16px;
}

.text-with-button {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  align-content: center;
}

.question-titles {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  white-space: nowrap;
}
</style>
