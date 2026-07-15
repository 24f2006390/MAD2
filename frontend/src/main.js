import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)


import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/bootstrap-icons/font/bootstrap-icons.min.css";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(router).use(pinia).mount("#app");
