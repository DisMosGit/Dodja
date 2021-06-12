import axios from "axios";

export default {
  state: {
    user: localStorage.getItem("user") || null,
    refresh_token: localStorage.getItem("refresh_token"),
    access_token: localStorage.getItem("access_token"),
    last_refresh: new Date(localStorage.getItem("last_refresh"))
  },
  getters: {
    user: state => {
      if (state.user) {
        return JSON.parse(state.user);
      }
      return null;
    },
    auth: state => {
      return Boolean(state.user);
    },
    refresh_token: state => {
      return state.refresh_token;
    },
    access_token: state => {
      return state.access_token;
    },
    last_refresh: state => {
      return state.last_refresh;
    },
    auth_header: state => {
      return "Bearer " + state.access_token;
    }
  },
  mutations: {
    saveSession: (state, payload) => {
      if (payload != null) {
        if (payload.user != null) {
          localStorage.setItem("user", JSON.stringify(payload.user));
          state.user = JSON.stringify(payload.user);
        }
        if (payload.access_token != null) {
          localStorage.setItem("access_token", payload.access_token);
          state.access_token = payload.access_token;
          localStorage.setItem("last_refresh", new Date());
          state.last_refresh = new Date(localStorage.getItem("last_refresh"));
        }
        if (payload.refresh_token != null) {
          localStorage.setItem("refresh_token", payload.refresh_token);
          state.refresh_token = payload.refresh_token;
        }
      } else {
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        state.user = null;
        state.access_token = null;
        state.refresh_token = null;
      }
    }
  },
  actions: {
    login: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post("/api-auth/json/login/", payload)
          .then(response => {
            console.log("login");
            context.commit("saveSession", {
              user: response.data.user,
              access_token: response.data.access_token,
              refresh_token: response.data.refresh_token
            });
            resolve(response);
          })
          .catch(error => {
            console.log("login", error.response.data);
            context.commit("saveSession");
            reject(error.response);
          });
      });
    },
    logout: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post("/api-auth/json/logout/", payload, {
            headers: {
              Authorization: context.getters.auth_header
            }
          })
          .then(response => {
            context.commit("saveSession");
            resolve(response);
          })
          .catch(error => {
            context.commit("saveSession");
            reject(error.response);
          });
      });
    },
    registration: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post("/api-auth/json/registration/", payload)
          .then(response => {
            console.log("registration");
            context.commit("saveSession", {
              user: response.data.user,
              access_token: response.data.access_token,
              refresh_token: response.data.refresh_token
            });
            resolve(response);
          })
          .catch(error => {
            console.log("registration", error.response.data);
            context.commit("saveSession");
            reject(error.response);
          });
      });
    },
    refreshToken: async (context, payload) => {
      if (payload == null) {
        payload = { refresh: context.state.refresh_token };
      }
      return new Promise((resolve, reject) => {
        axios
          .post("/api-auth/json/token/refresh/", payload)
          .then(response => {
            console.log("refresh");
            context.commit("saveSession", {
              access_token: response.data.access
            });
            resolve(response);
          })
          .catch(error => {
            console.log("refresh", error.response.data);
            context.commit("saveSession");
            reject(error.response);
          });
      });
    },
    getProfile: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post("/api-auth/json/user/", {
            data: payload,
            headers: { Authorization: "Bearer " + context.state.access_token }
          })
          .then(response => {
            console.log("refresh");
            context.commit("saveSession", {
              access_token: response.data.access
            });
            resolve(response);
          })
          .catch(error => {
            console.log("refresh", error.response.data);
            context.commit("saveSession");
            reject(error.response);
          });
      });
    }
  }
};
