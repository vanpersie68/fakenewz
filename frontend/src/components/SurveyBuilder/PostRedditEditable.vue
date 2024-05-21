<template>
  <div>
    <div class="post">
      <a v-if="isImage" :href="question.articleURL" target="_blank"
        ><img
          :src="question.articleImage"
          :alt="question.articleTitle"
          width="100%"
          height="auto"
      /></a>
      <div v-else class="no-image">{{ $t('postEditable.noImage') }}</div>
      <p @focusout="updateSource">
        {{ question.articleSource.toUpperCase() }}
      </p>
      <a :href="question.articleURL" target="_blank">
        <h1 @focusout="updateTitle">{{ question.articleTitle }}</h1>
      </a>
    </div>
    <line-base class="light" />

    <div class="comment">
      <div
        v-for="item in question.comments"
        :key="item.id"
        class="comment-item"
      >
        <div class="comment-content">
          <div @click="chooseAvatar(item.id)" style="flex-shrink: 0">
            <el-avatar :key="item.avatarUrl" :src="item.avatarUrl"></el-avatar>
          </div>
          <div style="margin-left: 10px; width: 100%">
            <el-input
              placeholder="Please enter a user name"
              size="small"
              v-model="item.username"
              @blur="updateComment(item)"
            ></el-input>
            <el-input
              placeholder="Please enter a comment"
              size="small"
              v-model="item.content"
              @blur="updateComment(item)"
            ></el-input>
          </div>
        </div>
        <!-- <button-base class="primary standard" :title="'del'" @buttonPress="delComment(item.id)"></button-base> -->
      </div>
      <line-base class="light" />
      <!-- 
      <label style="font-weight:600;">Add Comment</label>
      <div class="type-in">
        <el-input v-model="comment" placeholder="share your thoughts"></el-input>
        <button-base
        class="primary standard"
        :title="'Add'"
        @buttonPress="addComment"
        
      />

      </div> -->
      <ChooseAvatarModal
        v-if="dialogVisible"
        :dialogVisible.sync="dialogVisible"
        :currAvatarId="currAvatarId"
        @onChange="changeAvatar"
      />
    </div>
  </div>
</template>

<script>
import SurveyServices from '../../services/SurveyServices'
import store from '../../store/SurveyBuilder.js'
import ButtonBase from '../../components/ButtonBase.vue'
import LineBase from './LineBase.vue'
import ChooseAvatarModal from './ChooseAvatarModal.vue'

export default {
  name: 'PostFacebook',
  store: store,
  data() {
    return {
      comment: '',
      dialogVisible: false,
      currAvatarId: null,
    }
  },
  props: {
    question: Object,
  },
  components: {
    ButtonBase,
    LineBase,
    ChooseAvatarModal,
  },
  mounted() {
    console.log(this.question)
  },
  methods: {
    changeAvatar(id, v) {
      console.log(id, v)
      this.question.comments.find((el) => el.id === id).avatarUrl = v
    },
    chooseAvatar(id) {
      this.dialogVisible = true
      this.currAvatarId = id
    },
    async updateComment(it) {
      const res = await SurveyServices.patchComment(it.id, {
        content: it.content,
        username: it.username,
      })
    },
    async addComment() {
      if (this.question.comments?.length >= 2) {
        this.$alert('Max of 2 comments')
        return
      }
      const res = await SurveyServices.postComment(this.question.id, {
        content: this.comment,
      })
      console.log(res)
      this.question.comments.push(res)
    },

    async delComment(id) {
      const res = await SurveyServices.delComment(id)
      this.question.comments.splice(
        this.question.comments.findIndex((el) => el.id === id),
        1
      )
    },
    /**
     * Update and save source being changed
     */
    async updateSource(e) {
      store.commit('updateValue', {
        value: e.target.innerHTML,
        parent: this.question,
        key: 'articleSource',
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleSource: e.target.innerHTML,
      })
    },
    /**
     * Update and save title being changed
     */
    async updateTitle(e) {
      store.commit('updateValue', {
        value: e.target.innerHTML,
        parent: this.question,
        key: 'articleTitle',
      })

      await SurveyServices.patchQuestionType(this.question.id, {
        articleTitle: e.target.innerHTML,
      })
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

.comment {
}
.comment-item {
  display: flex;
  margin-bottom: 10px;
}
.comment-content {
  display: flex;
  margin-bottom: 10px;
  width: 90%;
}
.type-in {
  display: flex;
  align-items: center;
}

.post {
  width: 600px;
  background-color: #f0f2f5;
  border-bottom: 1px solid #ced0d4;
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
</style>
