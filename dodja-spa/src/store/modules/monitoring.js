import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    createMonitoringTask: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(
            `/api/host/${payload.host_id}/monitoring/?format=json`,
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
    getMonitoringTaskList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host_id}/monitoring/?format=json`, {
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
    getMonitoringTaskDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
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
    updateMonitoringTask: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .patch(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
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
    deleteMonitoringTask: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(
            `/api/host/${payload.host_id}/monitoring/${payload.id}/?format=json`,
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
