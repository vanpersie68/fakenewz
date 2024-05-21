<template>
  <div>
    <!-- For PC -->
    <div class="page1" v-if="PageType">
      <el-container class="content-boxPage1">
        <!--        <el-aside width="500px" class="content-aside">-->
        <!-- <el-aside width="50%" class="content-aside"> -->
        <el-aside class="content-aside">
          <h1>{{ $t('g5.Welcome to fakenewz Survey Platform!') }}</h1>
          <p>{{ $t('home.title1') }}</p>
          <p>{{ $t('home.title2') }}</p>
          <p>{{ $t('home.title3') }}</p>
          <div>
            <el-button plain icon="el-icon-s-promotion" @click="getStart">{{
              $t('home.getStart')
            }}</el-button>
            <el-button type="info" icon="el-icon-edit" @click="goToAnchor">{{
              $t('home.learnMore')
            }}</el-button>
          </div>
        </el-aside>
        <el-main style="text-align: center">
          <!--          <youtube width="550px" video-id="mlQuOl2ZVFY" ref="youtube"></youtube>-->
          <!-- <youtube resize="resizeFlag" fitParent="fitParentFlag" :video-id="videoId" :player-vars="playerVars"
            ref="youtube"> --> <!-- </youtube> -->
          <iframe width="100%" height="100%"
            src="https://www.youtube.com/embed/mlQuOl2ZVFY?si=muGwj-cjb_DDZzUH&amp;start=1" title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen></iframe>
        </el-main>
      </el-container>
    </div>
    <!-- For mobile -->
    <div class="page1" v-else>
      <!--        <el-aside width="500px" class="content-aside">-->
      <div class="boxForMobile">
        <h1>{{ $t('g5.Welcome to fakenewz Survey Platform!') }}</h1>
        <p>{{ $t('home.title1') }}</p>
        <p>{{ $t('home.title2') }}</p>
        <p>{{ $t('home.title3') }}</p>
        <div class="boxForMobile">
          <el-button plain icon=" el-icon-s-promotion" @click="getStart">{{
            $t('home.getStart')
          }}</el-button>
          <el-button type="info" icon="el-icon-edit" @click="goToAnchor">{{
            $t('home.learnMore')
          }}</el-button>
        </div>
      </div>
      <div class="boxForMobile">
        <!--          <youtube width="550px" video-id="mlQuOl2ZVFY" ref="youtube"></youtube>-->
        <!-- <youtube resize="resizeFlag" fitParent="fitParentFlag" :video-id="videoId" :player-vars="playerVars"
            ref="youtube"> --> <!-- </youtube> -->
        <iframe width="80%" height="90%" src="https://www.youtube.com/embed/mlQuOl2ZVFY?si=muGwj-cjb_DDZzUH&amp;start=1"
          title="YouTube video player" frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen></iframe>
      </div>
    </div>

    <div class="page2">
      <div class="content-box-cards">
        <div class="subtitle">
          <h1>{{ $t('home.functionIntro') }}</h1>
        </div>

        <el-carousel :interval="4000" height="270px">
          <div class="carousel-box">
            <el-carousel-item v-for="item in images" :key="item.title">
              <h1>{{ $t(item.title) }}</h1>
              <!-- PC -->
              <el-container v-if="PageType">
                <el-aside width="50%">
                  <ul v-for="i in item.info" :key="i">
                    <li>{{ $t(i) }}</li>
                  </ul>
                </el-aside>
                <el-main>
                  <img id="carousel-img" :src="item.url" height="200px" />
                </el-main>
              </el-container>
              <!-- Mobile -->
              <el-container v-else>
                <el-aside width="35%">
                  <ul v-for="i in item.info" :key="i">
                    <li>{{ $t(i) }}</li>
                  </ul>
                </el-aside>
                <el-main>
                  <img id="carousel-img" :src="item.url" height="200px" />
                </el-main>
              </el-container>
            </el-carousel-item>
          </div>
        </el-carousel>
      </div>
    </div>

    <!-- For PC -->
    <div id="page3" v-if="PageType">
      <div class="content-box">
        <div class="subtitle">
          <h1>{{ $t('home.learnMoreTitle') }}</h1>
          <p>{{ $t('home.learnMoreDes') }}</p>
        </div>
        <el-container class="content-boxPage1">
          <!--          <el-aside width="400px" style="margin-left: 80px">-->
          <el-aside width="40%" style="margin-left: 2vw">
            <h1>1. {{ $t('home.step1Title') }}</h1>
            <ul>
              <li>{{ $t('home.step1Des1') }}</li>
              <li>{{ $t('home.step1Des2') }}</li>
              <li>{{ $t('home.step1Des3') }}</li>
            </ul>
            <lottie :options="defaultOptions3" :width="240" :height="240" />
            <!-- style="position: relative; left: 100px; bottom: 60px" /> -->
          </el-aside>
          <el-main class="stepPicBox">
            <img src="./images/surveybuild.png" alt="" class="stepPic" />
          </el-main>
        </el-container>
      </div>
    </div>
    <!-- For mobile -->
    <div id="page3" v-else>
      <div class="subtitle">
        <h1>{{ $t('home.learnMoreTitle') }}</h1>
        <p>{{ $t('home.learnMoreDes') }}</p>
      </div>
      <div class="boxForMobile">
        <lottie :options="defaultOptions3" :width="200" :height="200" style="position: relative; right: px" />
      </div>
      <div class="boxForMobile">
        <h1>1. {{ $t('home.step1Title') }}</h1>
        <ul>
          <li>{{ $t('home.step1Des1') }}</li>
          <li>{{ $t('home.step1Des2') }}</li>
          <li>{{ $t('home.step1Des3') }}</li>
        </ul>
      </div>
      <div class="boxForMobile">
        <img src="./images/surveybuild.png" alt="" width="100%" />
      </div>
    </div>

    <!-- For PC -->
    <div class="page2" v-if="PageType">
      <div class="content-box">
        <el-container>
          <!--          <el-aside width="600px" style="margin-left: 30px">-->
          <el-aside style="width:50%">
            <img src="./images/publish.png" alt="" class="stepPic" />
          </el-aside>
          <el-main style="margin-left: 2vw">
            <h1>2. {{ $t('home.step2Title') }}</h1>
            <ul>
              <li>{{ $t('home.step2Des1') }}</li>
              <li>{{ $t('home.step2Des2') }}</li>
              <li>{{ $t('home.step2Des3') }}</li>
            </ul>
            <lottie :options="defaultOptions" :width="200" :height="200"
              style="position: relative; left: 100px; bottom: 20px" />
          </el-main>
        </el-container>
      </div>
    </div>
    <!-- For mobile -->
    <div class="page2" v-else>
      <!--          <el-aside width="600px" style="margin-left: 30px">-->
      <div>
        <lottie :options="defaultOptions" :width="200" :height="200" />
      </div>
      <div class="boxForMobile">
        <h1>2. {{ $t('home.step2Title') }}</h1>
        <ul>
          <li>{{ $t('home.step2Des1') }}</li>
          <li>{{ $t('home.step2Des2') }}</li>
          <li>{{ $t('home.step2Des3') }}</li>
        </ul>
      </div>
      <div class="boxForMobile">
        <img src="./images/publish.png" alt="" style="width: 100%" />
      </div>
    </div>

    <!-- For PC -->
    <div class="page1" v-if="PageType">
      <div class="content-box">
        <el-container>
          <el-aside width="500px">
            <div style="margin-left: 2vw">
              <!--              <div style="margin-left: 80px">-->
              <h1>3. {{ $t('home.step3Title') }}</h1>
              <ul>
                <li>{{ $t('home.step3Des1') }}</li>
                <li>{{ $t('home.step3Des2') }}</li>
                <li>{{ $t('home.step3Des3') }}</li>
              </ul>
            </div>
            <lottie :options="defaultOptions2" :width="200" :height="200" />
            <!--              style="position: relative; left: 100px; bottom: 20px" />-->
          </el-aside>
          <el-main class="stepPicBox">
            <img src="./images/result.png" alt="" class="stepPic" />
          </el-main>
        </el-container>
      </div>
    </div>
    <!-- For mobile -->
    <div class="page1" v-else>
      <div class="boxForMobile">
        <lottie :options="defaultOptions2" :width="200" :height="200" />
      </div>
      <div class="boxForMobile">
        <!--              <div style="margin-left: 80px">-->
        <h1>3. {{ $t('home.step3Title') }}</h1>
        <ul>
          <li>{{ $t('home.step3Des1') }}</li>
          <li>{{ $t('home.step3Des2') }}</li>
          <li>{{ $t('home.step3Des3') }}</li>
        </ul>
      </div>
      <!--              style="position: relative; left: 100px; bottom: 20px" />-->
      <div class="boxForMobile">
        <img src="./images/result.png" alt="" style="width: 100%" />
      </div>
    </div>

  </div>
</template>

<script src="vue-youtube/dist/vue-youtube.js"></script>
<script>
import Vue from 'vue'
import VueYoutube from 'vue-youtube'

import * as animationData from '@/assets/publish.json'
import * as animationData2 from '@/assets/analyse.json'
import * as animationData3 from '@/assets/create.json'

Vue.use(VueYoutube)

export default {
  data() {
    return {
      defaultOptions: { animationData: animationData.default },
      defaultOptions2: { animationData: animationData2.default },
      defaultOptions3: { animationData: animationData3.default },
      

      images: [
        {
          title: 'home.cardTitle1',
          info: [
            'home.card1Info1',
            'home.card1Info2',
            'home.card1Info3',
            'home.card1Info4',
            'home.card1Info5',
            'home.card1Info6',
          ],
          url: require('./images/carousels/bill payment.png'),
        },
        {
          title: 'home.cardTitle2',
          info: ['home.card2Info1', 'home.card2Info2', 'home.card2Info3'],
          url: require('./images/carousels/app development.png'),
        },
        {
          title: 'home.cardTitle3',
          info: [
            'home.card3Info1',
            'home.card3Info2',
            'home.card3Info3',
            'home.card3Info4',
            'home.card3Info5',
          ],
          url: require('./images/carousels/bill payment.png'),
        },
        {
          title: 'home.cardTitle4',
          info: ['home.card4Info1', 'home.card4Info2', 'home.card4Info3'],
          url: require('./images/carousels/analytics.png'),
        },
      ],

      // Page Type:PC/Mobile
      PageType: true,
      // Record the size of the screen
      screenWidth: null,
      // Flag for reload
      render: true
    }
  },
  mounted() {
    // When initialization, get the screen width
    window.addEventListener('load', this.checkWidth)
    //If the window size hange, reload the page
    window.addEventListener('resize', this.checkWidth)
    window.addEventListener('resize', this.reload)
  },
  destroyed() {
    window.removeEventListener('resize', this.reload)
  },
  computed:{
  },
  methods: {
    getStart() {
      this.$router.replace('/My_Survey')
    },
    goToAnchor() {
      this.$el.querySelector('#page3').scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    },
    // Reload the page
    reload() {
      this.render = false
      this.$nextTick(() => {
        this.render = true
      })
    },
    // Check the screen width
    checkWidth() {
      this.screenWidth = document.body.clientWidth
      console.log("screenwidth:" + this.screenWidth)
      if (this.screenWidth < 766) {
        this.PageType = false;
      }
      else {
        this.PageType = true;
      }
    }
  },
}
</script>

<style scoped>
/* Common Style */
#page3 {
  padding: 20px;
  background-color: #d3dce6;
  /* height: 500px; */
  color: #566370;
}

.page1 {
  padding: 20px;
  background-color: #d3dce6;
  /* height: 400px; */
  color: #566370;
}

.page2 {
  padding: 20px;
  background-color: #fff;
  /* height: 400px; */
  color: #566370;
}

.page1 .subtitle {
  text-align: center;
}

#page3 .subtitle {
  text-align: center;
}

.page2 .subtitle {
  text-align: center;
}

/* mobile */
@media only screen and (max-width: 767px) {
  h1 {
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    font-weight: bolder;
    font-size: x-large;
    color: #475669;
  }

  .content-boxPage1 {
    width: 100%;
    height: 100%;
    overflow: auto;
    /* padding-left: 2%; */
    /* padding: autoplay; */
    display: flex;
    flex-wrap: wrap;
  }

  .content-box {
    width: 100%;
    height: 100%;
    overflow: auto;
    /* padding-left: 2%;
    padding: autoplay;
    display: flex;
    flex-wrap: wrap; */
  }

  .content-aside {
    text-align: center;
    align-items: center;
    color: #566370;
    width: 100%;
  }

  .boxForMobile {
    width: 100%;
    align-items: center;
    text-align: center;
    padding: auto;
    margin-bottom: 2rem;
  }

  .lotForMobile {
    position: relative;
    width: 50%;
    height: 50%;
  }

  #carousel-img {
    position: relative;
    bottom: 60px;
    padding-left: 0%;
  }

  .carousel-box ul {
    position: relative;
    padding-left: 30%;
    bottom: 10px;
    /* left: 50rem; */
    /*font-size: 13px;*/
    font-size: medium;
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
  h1 {
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
      Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    font-weight: bolder;
    font-size: xx-large;
    color: #475669;
    /*font-size: 40px;*/
  }

  .content-box .content-box-cards {
    /*margin: 0 120px 0 120px;*/
    width: 100%;
    height: 100%;
    overflow: auto;
    /*padding-left: 2%;*/
    /*display: flex;*/
    /*flex-wrap: wrap;*/
  }

  .content-aside {
    text-align: right;
    color: #566370;
    width: 50%;
  }

  .content-aside div {
    text-align: center;
    margin-top: 50px;
  }

  .stepPicBox {
    text-align: right;
  }

  .stepPic {
    width: 100%px;
    max-width: 800px;
  }

  #carousel-img {
    position: relative;
    bottom: 60px;
    padding-left: 30%;
  }

  .carousel-box ul {
    position: relative;
    padding-left: 50%;
    bottom: 10px;
    /* left: 50rem; */
    /*font-size: 13px;*/
    font-size: medium;
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

.el-carousel__item h3 {
  color: #475669;
  font-size: medium;
  /*font-size: 14px;*/
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}



.carousel-box h1 {
  align-items: center;
  text-align: center;
  margin-left: 20px;
  font-size: 30px;
}
</style>
