<template>
  <nav>
        <router-link id="title" push to="/">{{ $t("fakenewz Survey Platform") }}</router-link>
        <!-- styling doesnt change to rtl if urdu selected atm, only if changed manually in i18n.js -->
        <lang-drop-down/>
        <!-- <button-base class="alternate min" :icon="'fas fa-user fa-me'" :title="$t('navBar.myAccount')"></button-base> -->
        <router-link v-show="isLogin === false" push to=/Login>{{ $t("g5.Log In") }}</router-link>
        <router-link v-show="isLogin === false" push to=/Signup>{{ $t("g5.Sign Up") }}</router-link>
        <!-- <router-link v-show="isLogin === true" replace to=/User>{{ $t("g5.User Profile") }}</router-link> -->
        <router-link v-show="isLogin === true" replace to=/User>{{ username }}</router-link>
        <router-link v-show="isLogin === true" replace to=/My_Survey>{{ $t("g5.My Surveys") }}</router-link>
    </nav>

</template>

<script>
/* Alternate Button Types */

import ButtonBase from '../components/ButtonBase.vue'
import LangDropDown from './LangDropDown.vue'
import pubsub from "pubsub-js";

export default {
  name: "TheNavBar",
  data() {
    return {
      isLogin: localStorage.getItem('token') != null ? true : false,
      username: localStorage.getItem('username')
    };
  },
  components: {
    ButtonBase,
    LangDropDown,
  },
  methods: {
    test() {
      console.log("OK")
    }
  },
  mounted() {
    //login
    this.loginPID = pubsub.subscribe("loginAction", (msgName, data) => {
      this.isLogin = data;
      this.username = localStorage.getItem("username");
      localStorage.setItem("isLogin",this.isLogin);
      console.log(msgName);
    });
    //logout
    this.logoutPID = pubsub.subscribe("logoutAction", (msgName, data) => {
      this.isLogin = data;
      console.log(msgName);
      localStorage.removeItem("username");
      localStorage.removeItem("isLogin");
    });
    //signup
    this.signupPID = pubsub.subscribe("signupAction", (msgName, data) => {
      this.isLogin = data;
      console.log(msgName);
      localStorage.setItem("isLogin",this.isLogin);
    });
  },
  beforeDestroy() {
    pubsub.unsubscribe(this.loginPID);
    pubsub.unsubscribe(this.logoutPID);
    pubsub.unsubscribe(this.signupPID);
  }
}
</script>

<style scoped>
nav {
  margin-top: 0px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  max-height: 56px;
  min-height: 56px;
  background-color: #566370;


  position: sticky;
  top: 0;
  z-index: 100;
}

#title {
  flex-grow: 2;
  margin-left: 20px;
  color: #fff;
}

a {
  text-decoration: none;
  color: #fff;
  padding: 10px 20px 10px 0;
}

a:hover {
  opacity: .3;
  transition: opacity 0.3s;
}

ul {
  list-style: none;
}
</style>
