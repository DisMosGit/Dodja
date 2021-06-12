import axios from "axios";

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    getMonitoringLogList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.monitoring_id}/log/?format=json`,
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
            console.log(error);
            reject(error.response);
          });
      });
    },
    getMonitoringLogDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(
            `/api/host/${payload.host_id}/monitoring/${payload.monitoring_id}/log/${payload.id}?format=json`,
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
    }
  }
};
