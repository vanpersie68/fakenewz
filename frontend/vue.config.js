const axios = require("axios");
const path = require('path')

function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  outputDir: "dist",
  assetsDir: "static",
  publicPath: process.env.BASE_URL,
  devServer: {
    proxy: process.env.VUE_APP_SERVER,
  },
  configureWebpack: {
    resolve: {
      fallback: {
        path: false
      }
    },
    module: {
      rules: [
        {
          test: /\.mjs$/,
          include: /node_modules/,
          type: "javascript/auto",
        },
      ],
    },
  },
  chainWebpack(config) {
    config.module.rule("svg").exclude.add(resolve("src/assets/icons/svg")).end();
    config.module
      .rule("icons")
      .test(/\.svg$/)
      .include.add(resolve("src/assets/icons/svg"))
      .end()
      .use("svg-sprite-loader")
      .loader("svg-sprite-loader")
      .options({
        symbolId: "icon-[name]",
      })
      .end();
  },
};

// The proxy address in vue.config.js is automatically used locally. BaseUrl is not required. Otherwise the agent will fail
if (process.env.VUE_APP_ENV !== "development") {
  axios.defaults.baseURL = process.env.VUE_APP_SERVER;
  axios.defaults.url = process.env.VUE_APP_WEBSITE;
}
