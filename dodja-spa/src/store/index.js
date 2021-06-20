import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import auth from "./modules/auth";
import hint from "./modules/hint";
import host from "./modules/host";
import job from "./modules/job";
import monitoring_log from "./modules/monitoring_log";
import monitoring from "./modules/monitoring";
import note from "./modules/note";
import access from "./modules/access";
import user from "./modules/user";
import profile from "./modules/profile";

Vue.use(Vuex);

axios.defaults.baseURL =
  window.location.protocol + "//" + window.location.hostname + ":" + "8000";

function notifyMe(title, text) {
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  } else if (Notification.permission === "granted") {
    new Notification(title, {
      body: text,
      icon: axios.defaults.baseURL + "/static/favicon.ico"
    });
  } else if (Notification.permission !== "denied") {
    Notification.requestPermission(function(permission) {
      if (permission === "granted") {
        new Notification(title, {
          body: text,
          icon: axios.defaults.baseURL + "/static/favicon.ico"
        });
      }
    });
  }
}

axios.interceptors.request.use(
  function(request) {
    request.headers.common["Access-Control-Expose-Headers"] = "X-WEBPUSH, ";
    request.headers.common["X-WEBPUSH"] = "all";
    return request;
  },
  function(error) {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  function(response) {
    if (response.headers["x-webpush"]) {
      try {
        JSON.parse(response.headers["x-webpush"]).forEach(element => {
          notifyMe(element.subject, element.message);
        });
      } catch (err) {
        console.log("push error", err);
      }
    }
    return response;
  },
  function(error) {
    if (error.response.status == 401) {
      localStorage.removeItem("user");
      location.reload();
    }
    return Promise.reject(error);
  }
);

export default new Vuex.Store({
  state: {
    message: "",
    language: "en"
  },

  getters: {
    message: state => {
      return state.message;
    },
    language: state => {
      return state.language;
    }
  },

  mutations: {
    setMsg: (state, message) => {
      console.log(message);
      state.message = message;
    },
    setLanguage: (state, language) => {
      state.language = language;
    }
  },

  actions: {},
  modules: {
    auth,
    hint,
    host,
    job,
    monitoring_log,
    monitoring,
    note,
    access,
    user,
    profile
  }
});
