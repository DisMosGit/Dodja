import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    getMonitoringTaskLogList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.monitoring_id}/log/?format=json`,
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
            console.log(error);
            reject(error.response);
          });
      });
    },
    getMonitoringTaskLogDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.monitoring_id}/log/${payload.id}?format=json`,
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
    deleteMonitoringTaskLog: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(
            `/api/host/${payload.host_id}/monitoring/${payload.monitoring_id}/log/${payload.id}?format=json`,
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
