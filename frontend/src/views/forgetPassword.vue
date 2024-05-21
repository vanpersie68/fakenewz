<template>
  <div>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale = 1.0,minimum-scale=1.0" />
    <div class="main">
      <!-- forgot password block -->
      <div class="window">
        <p class="title">{{ $t('g5.Forgot your password?') }}</p>
<!--        <img alt="" class="line" src="imagesine.png" />-->
        <p class="msg">{{ $t('g5.Please enter your email') }}</p>
        <input class="email-box" type="text" v-model="email" />
<!--        <img alt="" class="line-bottom" src="imagesine.png" />-->
        <button class="submit" @click="handleSubmit">
          {{ $t('g5.SUBMIT') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'forgetPassword',
  data() {
    return {
      email: '',
    }
  },
  methods: {
    handleSubmit() {
      this.$axios
        .post('account/password/reset/', {
          email: this.email,
          lang: localStorage.getItem('lang') || 'en',
        })
        .then((res) => {
          alert(
            'The password reset email was sent sucessfully, please check your email!',
            res
          )
          // console.log(res);
          this.$router.replace({ name: 'login' })
        })
        .catch((error) => {
          alert('Failed, please check if your email is valid.', error)
          window.location.reload()
        })
    },
  },
}
</script>

<style scoped>
.main {
  position: relative;
  /*height: 800px;*/
  height: 100%;
}

.background {
  width: 100%;
  height: 800px;
  position: relative;
}

.window {
  background-color: white;
  border-radius: 16px;
  padding: 3rem;
  border: 2px solid black;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999;
}
.title {
  font-family: 'Arial',serif;
  /*font-size: 24px;*/
  font-size: x-large;
  font-weight: 700;
  line-height: normal;
  color: black;
  /*margin-bottom: 39px;*/
  /*margin-left: 90px;*/
  margin: 0 auto;
  margin-bottom: 2rem;
}
/*.line {*/
/*  width: 432px;*/
/*  margin-bottom: 23px;*/
/*}*/

/*.line-bottom {*/
/*  width: 432px;*/
/*  margin-top: 20px;*/
/*  margin-bottom: 30px;*/
/*}*/
.msg {
  /*width: 400px;*/
  width: 100%;
  font-family: 'Arial',serif;
  /*font-size: 16px;*/
  font-size: 1rem;
  font-weight: 700;
  line-height: normal;
  color: dimgray;
  /*margin-bottom: 9px;*/
  margin-bottom: 0.8rem;
  /*margin: 0 auto;*/
  /*margin-left: 15px;*/
}
.email-box {
  /*width: 396px;*/
  width: 100%;
  /*height: 32px;*/
  height: 2rem;
  background-color: white;
  /*margin-bottom: 30px;*/
  margin-bottom: 3rem;
  /*margin-left: 15px;*/
  border-radius: 4px;
  border: 2px solid linen;
}
.submit {
  background: none;
  border: 1px solid black;
  /*margin-bottom: 18px;*/
  /*margin-left: 13px;*/
  margin: 0 auto;
  border-radius: 8px;
  /*padding: 13px 172px;*/
  padding: 1rem 11rem;
  font-family: 'Arial',serif;
  display: flex;
  align-items: center;
  font-size: 1rem;
  font-weight: 400;
  line-height: normal;
}
.submit:hover {
  opacity: 0.7;
  cursor: pointer;
}

/*mobile*/
@media only screen and (max-width: 767px) {
  .window{
    width: 60%;
  }
  .title{
    font-size: large;
  }

  .msg{
    font-size: small;
  }

  .submit{
    padding: 1rem 5rem;
  }

}

</style>
