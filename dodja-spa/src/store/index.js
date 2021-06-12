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

// axios.interceptors.response.use(
//   function(response) {
//     return response;
//   },
//   function(error) {
//     if (error.response.status == 401) {
//       localStorage.removeItem("user");
//       location.reload();
//     }
//     return Promise.reject(error);
//   }
// );

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
