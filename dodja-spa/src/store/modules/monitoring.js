import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    createMonitoring: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(
            `/api/host/${payload.host_id}/monitoring/?format=json`,
            payload,
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
    getMonitoringList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host_id}/monitoring/?format=json`, {
            params: payload,
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
    getMonitoringDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
            {
              data: payload,
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
    updateMonitoring: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .patch(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
            payload,
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
    deleteMonitoring: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
            {
              params: payload,
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
