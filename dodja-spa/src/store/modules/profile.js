import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    updateProfile: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(`/api/user/?format=json`, payload, {
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
    getProfile: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/user/?format=json`, {
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
    getMyAccess: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.id}/my_access/?format=json`, {
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
    }
  }
};
