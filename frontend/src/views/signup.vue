<template>
  <section>
    <div class="sign-up">
      <meta name="viewport" content="width-device-width, initial-scale=1.0" />
      <div class="ui">
        <!-- Sign-up box -->
        <p class="account">{{ $t('g5.Create Account') }}</p>
        <img alt="" class="line" src="imagesine.png" />
        <p class="inputbox">{{ $t('g5.Username') }}</p>
        <div>
          <input class="rec4" type="text" v-model="username" />
        </div>
        <p class="inputbox">{{ $t('g5.Email') }}</p>
        <div>
          <input class="rec1" type="text" v-model="email" />
        </div>
        <p class="inputbox">{{ $t('g5.Password') }}</p>
        <div>
          <input class="rec2" ref="input1" type="password" v-model="password1" />
          <font-awesome-icon class="eye" v-show="show1" @click="showPassword" icon="eye" />
          <font-awesome-icon class="eye" v-show="!show1" @click="showPassword" icon="eye-slash" />
        </div>
        <p class="inputbox">{{ $t('g5.Confirm password') }}</p>
        <div>
          <input class="rec3" ref="input2" type="password" v-model="password2" />
          <font-awesome-icon class="eye" v-show="show1" @click="showPassword" icon="eye" />
          <font-awesome-icon class="eye" v-show="!show1" @click="showPassword" icon="eye-slash" />
        </div>
        <div class="error">
          <div id="error-message"></div>
        </div>
        <img alt="" class="line" src="imagesine.png" />
        <div>
          <button @click="signupAction" class="signup">
            {{ $t('g5.SIGN UP') }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import pubsub from 'pubsub-js'
import SurveyServices from '../services/SurveyServices'

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      show1: false,
    }
  },
  methods: {
    async signupAction() {
      try {
        const response = await this.$axios.post('account/register/', {
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2,
        });

        alert('Sign up successful. Please verify your email!', response);

        // update user status
        pubsub.publish('disablesignupAction', true);

        // save token on local storage
        localStorage.setItem('token', response.data.key);

        // redirect to the user profile page
        if (this.$route.params.surveyid != null) {
          const key = await SurveyServices.getToken(this.email);
          alert(key)
          this.$router.push({
            name: 'accept_invitation',
            query: { key: key, id: this.$route.params.surveyid, email:  this.$route.params.emailId},
          });
        } else {
          this.$router.replace({
            name: 'login',
          });
        }
      } catch (error) {
        var messages = [];
        for (var key in error.response.data) {
          messages.push(
            this.$t('g5.' + error.response.data[key][0].replace(/\./g, '')) + '<br>'
          );
        }
        if (messages.length < 100) {
          document.getElementById('error-message').innerHTML = messages;
        } else {
          //document.getElementById('error-message').innerHTML = 'Sign up failed';
        }
      }
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
.sign-up {
  position: relative;
  height: 100%;
}


/* mobile */
@media only screen and (max-width: 767px) {

  .ui {
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
    transform: translate(-50%, 0%); */
    width: 80%;
    margin-top: 1rem;
    margin-left: 1.5rem;
    margin-right: 2rem;
    margin-bottom: 1rem;
  }

  .account {
    font-size: 24px;
    font-weight: 700;
    line-height: normal;
    color: black;
    margin-bottom: 0.5rem;
    text-align: center;
  }

  .line {
    width: 100%;
    margin-bottom: 15px;
  }

  .inputbox {
    width: 80%;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-bottom: 0.5rem;
  }

  .rec1 {
    width: 96%;
    height: 32px;
    background-color: white;
    margin-bottom: 0.5rem;
    margin-left: auto;
    margin-right: auto;
    border-radius: 4px;
    border: 2px solid linen;
  }

  /* password box */
  .rec2 {
    width: 84%;
    height: 32px;
    background-color: white;
    margin-bottom: 0.5rem;
    margin-left: auto;
    margin-right: auto;
    border-radius: 4px;
    border: 2px solid linen;
  }

  /* confirm password box */
  .rec3 {
    width: 84%;
    height: 32px;
    background-color: white;
    margin-bottom: 0.1rem;
    margin-left: auto;
    margin-right: auto;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .rec4 {
    width: 96%;
    height: 32px;
    background-color: white;
    margin-bottom: 0.5rem;
    margin-left: auto;
    margin-right: auto;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .eye {
    margin-left: 11px;
    cursor: pointer;
  }

  .error {
    background: #ffc199;
    /*Change background color*/
    border-left: 9px solid #ff6600;
    /*Change left border color*/
    color: #2c3e50;
    /*Change text color*/
    width: 96%;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    margin-bottom: 4px;
  }

  .signup {
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

  .signup:hover {
    opacity: 0.3;
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
@media only screen and (min-width: 768px) {
  .ui {
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
    margin-top: 50px;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 45px;
  }

  .account {
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

  .inputbox {
    width: 400px;
    font-size: 16px;
    font-weight: 700;
    line-height: normal;
    color: dimgray;
    margin-bottom: 9px;
  }

  .rec1 {
    width: 396px;
    height: 32px;
    background-color: white;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .rec2 {
    width: 366px;
    height: 32px;
    background-color: white;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .rec3 {
    width: 366px;
    height: 32px;
    background-color: white;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .rec4 {
    width: 396px;
    height: 32px;
    background-color: white;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 2px solid linen;
  }

  .eye {
    margin-left: 11px;
    cursor: pointer;
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

  .signup {
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

  .signup:hover {
    opacity: 0.3;
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
