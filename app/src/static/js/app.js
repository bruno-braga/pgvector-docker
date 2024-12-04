const { createApp, h } = Vue
const createInertiaApp = window.InertiaVue.createInertiaApp


createInertiaApp({
  resolve: name => {
    const pages = {
      'Home': Home
    }

    return pages[name]
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
})