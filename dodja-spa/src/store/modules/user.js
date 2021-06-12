import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    getUserList: async (context, payload) => {
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
    }
  }
};
