<template>
  <section>
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <div class="main">
      <div class="window">
        <p class="title">{{ $t('g5.Log in') }}</p>
        <img alt="" class="line" src="imagesine.png" />
        <p class="msg">{{ $t('g5.Username') }}</p>
        <!-- username inputbox-->
        <div>
          <input class="username-box" type="text" v-model="username" />
        </div>
        <p class="msg">{{ $t('g5.Password') }}</p>
        <!-- password inputbox -->
        <div>
          <input class="password-box" ref="input" type="password" v-model="password" />
          <font-awesome-icon class="eye" v-show="show" @click="showPassword" icon="eye" />
          <font-awesome-icon class="eye" v-show="!show" @click="showPassword" icon="eye-slash" />
        </div>

        <div class="error">
          <div id="error-message"></div>
        </div>
        <!-- forget password -->
        <a class="forgot" @click="forgetPassword">{{
          $t('g5.Forgot your password?')
        }}</a>
        <!-- login button -->
        <div>
          <button @click="loginAction" class="loginButton">
            {{ $t('g5.LOG IN') }}
          </button>
        </div>
        <img alt="" class="line" src="imagesine.png" />
        <div class="bottom">
          <p class="havenoaccount">{{ $t('g5.Dont have an account?') }}</p>
          <div>
            <button @click="signup" class="signupButton">
              {{ $t('g5.SIGN UP') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import {reqLogin} from '../api'
import pubsub from 'pubsub-js'
export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      show: false,
      // alertText: '',
      // alertShow: false,
    }
  },
  methods: {
    loginAction() {
      this.$axios
        .post('account/login/', {
          username: this.username,
          password: this.password,
        })
        .then((res) => {
          // alert("Login successful", res.name);
          //update user status
          pubsub.publish('loginAction', true)
          //save token on local storage
          localStorage.setItem('token', res.data.key)
          localStorage.setItem('username', this.username)
          //redirect to the user profile page
          this.$router.replace({
            name: 'mySurvey',
          })
        })
        .catch((reason) => {
          // alert("Login failed\n"+ JSON.stringify(reason.response.data))
          var messages = []
          for (var key in reason.response.data) {
            messages.push(reason.response.data[key][0] + '<br>')
          }

          document.getElementById('error-message').innerHTML =
            this.$t('Log in failed') + ': ' + messages
        })
    },
    forgetPassword() {
      this.$router.push({ name: 'forget_password' })
    },
    // async login () {
    //   let res
    //   const {username, password} = this
    //   res = await reqLogin({username, password})
    //   if (res.code === 0) {
    //     this.$router.replace({
    //       name: "user"
    //     })
    //   }
    // },
    signup() {
      this.$router.replace({
        name: 'signup',
      })
    },
    showPassword() {
      if (this.show == false) {
        this.$refs.input.type = 'text'
        this.show = !this.show
      } else {
        this.$refs.input.type = 'password'
        this.show = !this.show
      }
    },
  },
  // showAlert(alertText) {
  //   this.alertShow = true
  //   this.alertText = alertText
  // }
}
</script>

<style scoped>
.main {
  position: relative;
  height: 100%;
}


/* mobile */
@media only screen and (max-width: 767px) {
  .window {
    background-color: white;
    border-radius: 16px;
    padding: 0.5rem;
    border: 2px solid black;
    /* display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-54%, -1%); */
    width: 80%;
    margin-top: 1rem;
    margin-left: 1.5rem;
    margin-right: 2rem;
    margin-bottom: 1rem;
  }

  .title {
    font-size: 24px;
    font-weight: 700;
    line-height: normal;
    color: black;
    margin-bottom: 0.5rem;
    text-align: center;
  }

  .line {
    width: 60%;
    margin-bottom: 15px;
  }

  .msg {
    width: 90%;
    font-size: 1rem;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-bottom: 0.8rem;
  }

  .username-box {
    width: 85%;
    height: 32px;
    background-color: white;
    margin-bottom: 1rem;
    margin-left: 1rem;
    margin-right: 1rem;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .password-box {
    width: 70%;
    height: 32px;
    background-color: white;
    margin-bottom: 1rem;
    margin-left: 1rem;
    margin-right: 1rem;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .eye {
    /* margin-left: 1rem; */
    cursor: pointer;
  }

  .forgot {
    display: block;
    font-family: 'Arial';
    font-size: 0.6rem;
    font-weight: 700;
    line-height: normal;
    color: rgba(13, 13, 209, 0.753);
    text-decoration: underline;
    margin-bottom: 2rem;
    cursor: pointer;
    text-align: center;
  }

  .loginButton {
    background: none;
    border: 1px solid black;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 0.5rem;
    border-radius: 8px;
    padding: 1rem 6rem;
    display: flex;
    align-items: center;
    font-size: 16px;
    font-weight: 400;
    line-height: normal;
  }

  .loginButton:hover {
    opacity: 0.3;
    cursor: pointer;
  }

  .bottom {
    display: flex;
    align-items: center;
  }

  .havenoaccount {
    width: 50;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-left: 2rem;
    margin-right: 2rem;
    text-align: center;
  }

  .error {
    background: #ffc199;
    /*Change background color*/
    border-left: 9px solid #ff6600;
    /*Change left border color*/
    color: #2c3e50;
    /*Change text color*/
    width: 90%;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    margin-bottom: 4px;
  }

  .signupButton {
    background: none;
    border: 1px solid black;
    border-radius: 8px;
    padding: 13px 28px 13px 28px;
    display: flex;
    margin-left: 3rem;
    align-items: center;
  }

  .signupButton:hover {
    opacity: 0.7;
    cursor: pointer;
  }
}

/* PAD creen
@media only screen and (min-width: 768px) {
  .content-box {
    /* margin: 0 120px 0 120px;*/
/* width: 100%;
    height: 100%;
    overflow: auto; */
/*padding-left: 2%;*/
/*display: flex;*/
/*flex-wrap: wrap;*/
/* }
} */

/* PC with common size screen */
@media only screen and (min-width: 992px) {
  .window {
    background-color: white;
    border-radius: 16px;
    padding: 20px 0 18px;
    border: 2px solid black;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, 0%);
    width: 450px;
    margin-top: 25px;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 25px;
  }

  .title {
    font-size: 24px;
    font-weight: 700;
    line-height: normal;
    color: black;
    margin-bottom: 25px;
  }

  .line {
    width: 100%;
    margin-bottom: 15px;
  }

  .msg {
    width: 400px;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-bottom: 9px;
  }

  .username-box {
    width: 396px;
    height: 32px;
    background-color: white;
    margin-bottom: 20px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .password-box {
    width: 366px;
    height: 32px;
    background-color: white;
    margin-bottom: 20px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .eye {
    margin-left: 11px;
    cursor: pointer;
  }

  .forgot {
    font-family: 'Arial';
    font-size: 14px;
    font-weight: 700;
    line-height: normal;
    color: rgba(13, 13, 209, 0.753);
    text-decoration: underline;
    margin-bottom: 31px;
    cursor: pointer;
  }

  .loginButton {
    background: none;
    border: 1px solid black;
    margin-bottom: 18px;
    border-radius: 8px;
    padding: 13px 160px;
    display: flex;
    align-items: center;
    font-size: 16px;
    font-weight: 400;
    line-height: normal;
  }

  .loginButton:hover {
    opacity: 0.3;
    cursor: pointer;
  }

  .bottom {
    display: flex;
    align-items: center;
  }

  .havenoaccount {
    width: 180px;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-right: 26px;
  }

  .error {
    background: #ffc199;
    /*Change background color*/
    border-left: 9px solid #ff6600;
    /*Change left border color*/
    color: #2c3e50;
    /*Change text color*/
    width: 90%;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    margin-bottom: 4px;
  }

  .signupButton {
    background: none;
    border: 1px solid black;
    border-radius: 8px;
    padding: 13px 28px 13px 28px;
    display: flex;
    align-items: center;
  }

  .signupButton:hover {
    opacity: 0.7;
    cursor: pointer;
  }

}

/* PC with large screen */
/* @media only screen and (min-width: 1360px) {
  h1 {
    color: red;
  } 

/* 
  .content-box {
    /*margin: 0 120px 0 120px;*/
/* width: 96%;
    overflow: auto;
    padding-left: 2%;
    padding-right: 2%; */
/*display: flex;*/
/*flex-wrap: wrap;*/
/* }
} */
</style>
