<template>
  <div class="main">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <div class="window">
      <!-- Reset password block -->
      <p class="title">{{ $t('g5.Reset your password') }}</p>
      <!--      <img alt="" class="line" src="imagesine.png" />-->
      <p class="msg">{{ $t('g5.Enter new password') }}</p>
      <div class="combo">
        <input class="input-box" ref="input1" type="password" v-model="password" />
        <font-awesome-icon class="eye" v-show="show1" @click="showPassword" icon="eye" />
        <font-awesome-icon class="eye" v-show="!show1" @click="showPassword" icon="eye-slash" />
      </div>
      <p class="msg">{{ $t('g5.Confirm your password') }}</p>
      <div class="combo">
        <input class="input-box" ref="input2" type="password" v-model="confirmPassword" />
        <font-awesome-icon class="eye" v-show="show1" @click="showPassword" icon="eye" />
        <font-awesome-icon class="eye" v-show="!show1" @click="showPassword" icon="eye-slash" />
      </div>
      <!--      <img alt="" class="line" src="imagesine.png" />-->
      <button class="submit" @click="handleSubmit">
        {{ $t('g5.SUBMIT') }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'resetPassword',
  data() {
    return {
      password: '',
      confirmPassword: '',
      uid: this.$route.query.uid,
      token: this.$route.query.token,
      show1: false,
    }
  },
  methods: {
    handleSubmit() {
      this.$axios
        .post('/account/password/reset/confirm/', {
          new_password1: this.password,
          new_password2: this.confirmPassword,
          uid: this.uid,
          token: this.token,
        })
        .then((res) => {
          alert('Congratulation, reset password successfully!', res)
          this.$router.replace({ name: 'login' })
        })
        .catch((err) => {
          let error = err.response.data.Message
          let errorMessage = ''
          for (let i = 0; i < error.length; i++) {
            if (error[i] === 1) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg1')
            }
            if (error[i] === 2) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg2')
            }
            if (error[i] === 3) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg3')
            }
            if (error[i] === 4) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg4')
            }
            if (error[i] === 5) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg5')
            }
            if (error[i] === 6) {
              errorMessage = errorMessage + this.$t('forgetpwd.msg6')
            }
          }
          alert(errorMessage)
        })
    },
    showPassword() {
      if (this.show1 == false) {
        this.$refs.input1.type = 'text'
        this.$refs.input2.type = 'text'
        this.show1 = !this.show1
      } else {
        this.$refs.input1.type = 'password'
        this.$refs.input2.type = 'password'
        this.show1 = !this.show1
      }
    },
  },
}
</script>

<style scoped>
.main {
  position: relative;
  height: 100%;
}

.window {
  background-color: white;
  border: 2px solid black;
  border-radius: 16px;
  padding: 3rem;
  /*display: flex;*/
  /*flex-direction: column;*/
  /*align-items: flex-start;*/
  /*position: fixed;*/
  /*top: 50%;*/
  /*left: 50%;*/
  /*transform: translate(-50%, -50%);*/
  /*z-index: 999;*/
  width: 30%;
  margin: 0 auto;
  margin-top: 3.5rem;
}

.title {
  font-size: x-large;
  font-weight: 700;
  line-height: normal;
  color: black;
  /*margin-bottom: 39px;*/
  /*margin-left: 90px;*/
}


.msg {
  width: 70%;
  font-size: 1rem;
  font-weight: 700;
  line-height: normal;
  color: dimgray;
  margin-bottom: 0.8rem;
}

.input-box {
  width: 85%;
  height: 2rem;
  background-color: white;
  margin-bottom: 3rem;
  border-radius: 4px;
  border: 2px solid linen;
  display: inline-block;
}

.eye {
  /*margin-left: 11px;*/
  /*margin-right: 15px;*/
  float: right;
  cursor: pointer;
  display: inline-block;
  margin: 0 auto;
  height: 2rem;
  /*transform: translate(50%, 50%);*/
}

.combo {
  width: 100%;
}

.submit {
  background: none;
  border: 1px solid black;
  margin: 0 auto;
  border-radius: 8px;
  padding: 1rem 11rem;
  font-family: 'Arial', serif;
  display: flex;
  align-items: center;
  font-size: 1rem;
  font-weight: 400;
  line-height: normal;
}

.submit:hover {
  opacity: 0.3;
  cursor: pointer;
}

/*mobile*/
@media only screen and (max-width: 767px) {
  .window {
    width: 60%;
    padding: 2rem;

  }

  .title {
    font-size: large;
  }

  .msg {
    font-size: small;
  }

  .combo {
    width: 100%;
  }

  /*.eye{*/
  /*  transform: translate(0,0);*/
  /*}*/

  .submit {
    padding: 1rem 5rem;
  }

}
</style>
