import axios from "axios";

export default {
  state: {
    loadedHints: []
  },
  getters: {
    loadedHints: state => {
      return state.loadedHints;
    }
  },
  mutations: {
    saveNewHint: (state, payload) => {
      state.loadedHints.push(payload);
    },
    editHintByID: (state, payload) => {
      state.loadedHints.every(function(hint, index) {
        if (hint.id == payload.id) {
          state.loadedHints[index] = payload;
          return false;
        } else return true;
      });
    },
    deleteLatestHint: state => {
      state.loadedHints.shift();
    },
    deleteHintByKey: (state, key) => {
      state.loadedHints.splice(
        state.loadedHints.indexOf(x => x.key == key),
        1
      );
    },
    deleteAllHints: state => {
      state.loadedHints = [];
    }
  },
  actions: {
    getHintList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/hint/?format=json`, {
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
    getHintDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/hint/${payload.key}/?format=json`, {
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
    loadHint: async (context, key) => {
      return new Promise((resolve, reject) => {
        if (!context.getters.loadedHints.find(x => x.key === key)) {
          context
            .dispatch("getHintDetail", { key: key })
            .then(response => {
              context.commit("saveNewHint", response.data);
              resolve(true);
            })
            .catch(error => {
              this.setMsg("hint error: " + JSON.stringify(error.data));
              reject(false);
            });
        }
      });
    }
  }
};
