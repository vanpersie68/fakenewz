<template>
  <body>
    <img :src="imgSrc" width="100%" height="100%" alt="" />

    <div class="box">
      <h1>Thanks for your participation</h1>
    </div>
  </body>
</template>

<script>
export default {
  name: 'Success',

  data() {
    return {
      imgSrc: require('./images/success.jpg'),
    }
  },
}
</script>

<style scoped>
.background {
}
body {
  width: 100%;
  height: 100%;
  z-index: -1;
  position: absolute;
}

@media (min-width: 890px) {
  h1 {
    color: #ffffff;
    text-transform: uppercase;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    margin: 0;
    padding: 0;
    font-size: 10em;
    text-align: center;
    text-shadow: 0px 5px 20px rgba(0, 0, 0, 1);
    mix-blend-mode: overlay;
  }
}
@media (max-width: 889px) {
  h1 {
    color: #ffffff;
    text-transform: uppercase;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    margin: 0;
    padding: 0;
    font-size: 50px;
    text-align: center;
    text-shadow: 0px 5px 20px rgba(0, 0, 0, 1);
    mix-blend-mode: overlay;
  }
}
</style>
