
export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/icon?family=Material+Icons"
      },
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: ["assets/style/main.css"],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxtjs/moment'
  ],
  moment: {
    locales: ['ru'],
    defaultTimezone: 'Europe/Moscow'
  },
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    "nuxt-quasar",
    // ["@nuxtjs/proxy", { pathRewrite: { "^/api": "/api" } }]
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: 'http://nxing:8000/',
    browserBaseURL: 'http://localhost:8000/',
    // proxyHeaders: false,
    // credentials: false,
    headers: {
      common: {

        // 'Origin':'http://localhost:3000/'

        // 'Access-Control-Allow-Origin': 'http://localhost:8000'

      }
    }
  },
  quasar: {
    // animations: ["fadeIn", "fadeOut"],
    framework: {
      iconSet: "fontawesome-v5",
      lang: 'rus',

      // config: {
      //   brand: {
      //     primary: "#ffffff",
      //     // ...
      //   },
      // },
      components: [
        'QBadge',
        'QTabPanels',
        'QTabPanel',
        'QPopupProxy',
        'QSplitter',
        "QTime",
        'QTh',
        'QTr',
        'QTd',
        'QSlideItem',
        "QList",
        "QItem",
        "QItemSection",
        "QItemLabel",
        "QChip",
        "QTabs",
        "QTab",
        "QRouteTab",
        "QForm",
        "QInput",
        "QToggle",
        "QIcon",
        "QBtn",
        "QBtnToggle",
        'Notify',
        'QTable',
        'QDate'
      ],
      directives: [
        'ClosePopup'
      ],
      // directives: ["ClosePopup"],
      // plugins: ["Cookies"],
      // iconSet: "fontawesome-v5",
      cssAddon: true
    },
    supportIE: true,
    htmlVariables: {}
  },
  transition: {
    name: "fade",
    mode: "out-in"
  },

  // proxy: {
  //   "/api": "http://nginx:8000/"
  // },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  },
  // router: {
  //   middleware:'auth'
  //   //   linkActiveClass: 'active',
  //   //   extendRoutes(routes, resolve) {
  //   //     routes.push({
  //   //       path: '*',
  //   //       component: resolve(__dirname, 'pages/index.vue ')
  //   //     })
  //   //   }
  // }
}
