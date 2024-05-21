<template>
  <el-dialog title="Select avatar" :visible.sync="dialogVisible" width="70%" :close-on-click-modal="false" :close-on-press-escape="false" :show-close="false">
    <div class="wrapper">
      <div class="list">
        <h3 style="margin-top: 0;">My Avatars</h3>
        <div class="list-scroll">
          <div class="avatar" v-for="a,i in avatars" :key="a.url">
            <img :src="a.url" @click="handelChoose(a)" class="item">
            <a style="cursor:pointer;color:red;" @click="handelDel(a)">DEL</a>
          </div>
        </div>
      </div>
      <el-upload class="upload-demo" drag action="/api/common/upload" :on-change="handleChange" multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Drag file here or <em>click upload</em></div>
        <div class="el-upload__tip" slot="tip">Only support jpg/png file,max 500 kb</div>
      </el-upload>
    </div>


    <span slot="footer" class="dialog-footer">
      <el-button @click="$emit('update:dialogVisible', false)">cancel</el-button>
      <el-button type="primary" @click="$emit('update:dialogVisible', false)">confirm</el-button>
    </span>
  </el-dialog>
</template>


<script>
import SurveyServices from "../../services/SurveyServices";

export default {
  name: "ChooseAvatarModal",
  data(){
    return{
      avatars: []

    }
  },
  props: {
    dialogVisible: Boolean,
    currAvatarId: Number,
  },
  mounted() {
    this.init()
  },
  methods: {
    handelDel(a){
      SurveyServices.deleteAvatar(a).then(() => {
        this.init()
      })
    },
    handleChange(file, fileList) {
      console.log(file, fileList)
      if (!file.response) return
      SurveyServices.postAvatar({
        url: file.response.value,
        user: localStorage.getItem('username'),
      })
      SurveyServices.patchComment(this.currAvatarId, {
        avatarUrl: file.response.value
      })
      this.$emit('onChange', this.currAvatarId, file.response.value)
      setTimeout(() => {
      this.init()
        
      }, 1000);
    },
    init() {
      SurveyServices.getAvatar({
          user: localStorage.getItem('username'),
        }).then((r) => {
          // this.$set(this,'avatars',r)
          this.avatars = r
        })
    },
    handelChoose(a) {
      SurveyServices.patchComment(this.currAvatarId, {
        avatarUrl: a.url
      })
      this.$emit('onChange', this.currAvatarId, a.url)
      this.$emit('update:dialogVisible', false)
      this.$alert('Edit success')
    },
  },


};
</script>


<style scoped>
.wrapper {
  display: flex;
}

.upload-demo {
  width: 400px;
}

.list {
  width: 300px;

}

.list-scroll {
  overflow-y: auto;
  height: 200px;
  display: flex;
  flex-wrap: wrap;
}

.item {
  width: 40px;
  height: 40px;
  border-radius: 20px;
  margin: 4px;
  cursor: pointer;
}
.avatar {
  display: inline-block;
  display: flex;
  flex-direction: column;
  align-items: center;

}
</style>
