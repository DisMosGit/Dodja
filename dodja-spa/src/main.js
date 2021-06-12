import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueI18n from "vue-i18n";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import HintBtn from "@/components/HintBtn";

Vue.use(VueI18n);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.filter("cut", function(value, from, to) {
  return String(value).slice(from, to);
});

Vue.filter("dockerNames", function(value) {
  var result = "";
  if (value) {
    value.forEach(function(entry) {
      result += `${entry.slice(1)}; `;
    });
  }
  return result;
});

Vue.filter("dockerPorts", function(value) {
  var result = "";
  if (value) {
    value.forEach(function(entry) {
      result += `${entry.IP}:${entry.PublicPort}->${entry.PrivatePort}; `;
    });
  }
  return result;
});

Vue.filter("dockerMounts", function(value) {
  var result = "";
  if (value) {
    value.forEach(function(entry) {
      result += `${entry.Destination}:${entry.Source || "~/"}; `;
    });
  }
  return result;
});

Vue.filter("toDate", function(value, type) {
  if (!type) return new Date(value).toLocaleDateString();
  else if (type === "ms") return new Date(value * 1000).toLocaleDateString();
});

Vue.filter("getValue", function(value, find_key) {
  return Object.keys(value).find(key => value[key] === find_key);
});

Vue.filter("mergeR", function(value, str) {
  return String(value) + String(str);
});

Vue.filter("mergeL", function(value, str) {
  return String(str) + String(value);
});

Vue.filter("capitalize", function(value) {
  return value.replace(/^./, c => c.toUpperCase());
});

Vue.config.productionTip = false;

router.beforeEach((to, from, next) => {
  if (to.name == "Registration") next();
  else if (to.name !== "Login" && !store.getters.auth)
    next({ name: "Login", query: { next: to.name } });
  else next();
});

Vue.component("HintBtn", HintBtn);

const i18n = new VueI18n({
  locale: "en",
  messages: {
    en: {
      language: "english",
      article: "a | an | the",
      list: "list",
      detail: "detail",
      update: "update",
      create: "create",
      delete: "delete",
      read: "read",
      new: "new",
      add: "add | adding",
      edit: "edit | editing",
      remove: "remove",
      reset: "reset",
      close: "close",
      open: "open",
      cancel: "cancel",
      refresh: "refresh",
      loading: "loading",
      login: "login",
      logout: "logout",
      registration: "registration",
      docker: "Docker",
      host: "host | hosts",
      monitoring: "monitoring",
      hint: "hint | hints",
      note: "note | notes",
      access: "access | accesses",
      permission: "permission | permissions",
      user: "user | users",
      task: "task | tasks",
      log: "log | logs",
      history: "history",
      profile: "profile"
    },
    ru: {
      language: "русский",
      article: "| | |",
      list: "список",
      detail: "подробно",
      update: "редактировать",
      create: "создать",
      delete: "уничтожить",
      read: "читать",
      new: "новый",
      add: "добавить | добавление",
      edit: "изменить | изменение",
      remove: "удалить",
      reset: "сбросить",
      close: "закрыть",
      open: "открыть",
      cancel: "отменить",
      refresh: "перезагрузить",
      loading: "загрузка",
      login: "вход",
      logout: "выход",
      registration: "регистрация",
      docker: "Docker",
      host: "узел | узлы",
      monitoring: "мониторинг",
      hint: "подсказка | подсказки",
      note: "заметка | заметки",
      access: "доступ | доступа",
      permission: "право | права",
      user: "пользователь | пользователи",
      task: "задача | задачи",
      log: "запись | записи",
      history: "история",
      profile: "профиль",
      settings: "настройки",
      description: "описание",
      title: "название",
      credentials: "реквизиты"
    }
  }
});

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount("#app");
