<template>
  <div class="main">
    <meta name="viewport" content="width-device-width, initial-scale=1.0" />
    <!-- Verify Email UI -->
    <div class="window">
      <p class="title">{{ $t('g5.Verify your email') }}</p>
      <button class="submit" @click="handleSubmit">{{ $t('Verify') }}</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'verifyEmail',
  data() {
    return {
      key: this.$route.query.key,
    }
  },
  methods: {
    handleSubmit() {
      this.$axios
        .post('/account/register/verify-email/', {
          key: this.key,
        })
        .then((res) => {
          alert('Congratulation, verify email successfully!', res)
          this.$router.replace({ name: 'login' })
        })
        .catch((err) => {
          alert('Expired link!', err)
          window.location.reload()
        })
    },
  },
}
</script>

<style scoped>
.main {
  position: relative;
  height: 800px;
}

.background {
  width: 100%;
  height: 800px;
  position: relative;
}
.copyright {
  color: white;
  position: absolute;
  left: 560px;
  bottom: 0px;
  display: center;
  text-align: center;
}
.window {
  background-color: white;
  border-radius: 16px;
  padding: 20px 0 18px;
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
  font-size: 24px;
  font-weight: 700;
  line-height: normal;
  color: black;
  margin-bottom: 39px;
  margin-left: auto;
  margin-right: auto;
}
.line {
  width: 432px;
  margin-bottom: 23px;
}

.line-bottom {
  width: 432px;
  margin-top: 20px;
  margin-bottom: 30px;
}
.msg {
  width: 400px;
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  color: dimgray;
  margin-bottom: 9px;
  margin-left: 15px;
}
.input-box {
  width: 396px;
  height: 32px;
  background-color: white;
  margin-bottom: 30px;
  margin-left: 15px;
  border-radius: 4px;
  border: 2px solid linen;
}
.submit {
  background-color: rgba(153, 105, 15, 0.493);
  margin-bottom: 18px;
  margin-left: 13px;
  margin-right: 13px;
  border-radius: 8px;
  padding: 13px 172px;
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
}
.submit:hover {
  background-color: blanchedalmond;
  cursor: pointer;
}
</style>
