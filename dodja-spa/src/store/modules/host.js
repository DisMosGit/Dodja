import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    createHost: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post("/api/host/?format=json", payload, {
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            console.log(error.response);
            reject(error.response);
          });
      });
    },
    getHostList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get("/api/host/?format=json", {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            console.log(error);
            reject(error.response);
          });
      });
    },
    getHostDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.id}/?format=json`, {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    updateHost: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .patch(`/api/host/${payload.id}/?format=json`, payload.data, {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    deleteHost: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(`/api/host/${payload.id}/?format=json`, {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    executeHost: async (context, payload) => {
      console.log("payload", payload);
      return new Promise((resolve, reject) => {
        if (!payload.data || !payload.data.command) {
          reject("command NotFound");
        } else {
          axios
            .post(
              `/api/host/${payload.id}/execute/?format=json`,
              payload.data,
              {
                params: payload.params,
                headers: {
                  Authorization: context.rootGetters.auth_header
                }
              }
            )
            .then(response => {
              resolve(response);
            })
            .catch(error => {
              reject(error.response);
            });
        }
      });
    }
  }
};
