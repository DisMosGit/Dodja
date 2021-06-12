import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    createAccess: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(
            `/api/host/${payload.host_id}/access/?format=json`,
            payload.data,
            {
              headers: {
                Authorization: context.rootGetters.auth_header
              }
            }
          )
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            console.log(error.response);
            reject(error.response);
          });
      });
    },
    getAccessList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host_id}/access/?format=json`, {
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
    getAccessDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/access/${payload.id}/?format=json`,
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
      });
    },
    updateAccess: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .patch(
            `/api/host/${payload.host_id}/access/${payload.id}/?format=json`,
            payload.data,
            {
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
      });
    },
    deleteAccess: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(
            `/api/host/${payload.host_id}/access/${payload.id}/?format=json`,
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
      });
    }
  }
};
