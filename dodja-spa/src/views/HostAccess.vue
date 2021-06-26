<template>
  <b-container class="my-2 p-2 shadow-sm">
    <h2 class="text-center">
      {{ $tc("access", 1) | capitalize
      }}<HintBtn hint_key="ru_host_access"></HintBtn>
      <b-badge @click="goRefreshAccess">
        <b-icon-arrow-repeat></b-icon-arrow-repeat>
      </b-badge>
    </h2>
    <AccessConfig
      v-for="access in accesses"
      v-bind:key="access.id"
      v-bind:access="access"
      @updateMe="tryUpdate"
      @deleteMe="tryDelete"
    ></AccessConfig>
    <b-row class="my-1">
      <b-col cols="7" class="px-1">
        <b-dropdown
          variant="white"
          class="border"
          :text="choice_user.username"
          lazy
          block
          menu-class="w-100"
        >
          <b-dropdown-item @click="tryRefreshUserList">
            {{ $tc("refresh", 1) | capitalize }}
          </b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item
            v-for="user in users"
            v-bind:key="user.id"
            @click="choiceUser(user)"
          >
            {{ user.username }}
          </b-dropdown-item>
        </b-dropdown>
      </b-col>
      <b-col cols="3" class="px-1">
        <b-form-input
          :placeholder="$tc('permission', 2) | capitalize"
          v-model="choice_permissions"
        ></b-form-input>
      </b-col>
      <b-col cols="2" class="px-1">
        <b-button-group>
          <b-button variant="success" @click="tryCreate()">
            <b-icon-plus-circle></b-icon-plus-circle>
          </b-button>
          <b-button variant="danger" @click="refreshChoice()">
            <b-icon-trash></b-icon-trash>
          </b-button>
        </b-button-group>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapActions } from "vuex";
import AccessConfig from "@/components/AccessConfig";

export default {
  name: "HostAccess",
  components: {
    AccessConfig
  },
  props: {
    settings: Object,
    host_id: String
  },
  data() {
    return {
      accesses: [],
      users: [],
      choice_user: {
        username: "username"
      },
      choice_permissions: 0
    };
  },
  methods: {
    ...mapActions([
      "createAccess",
      "getAccessList",
      "updateAccess",
      "deleteAccess",
      "getUserList"
    ]),
    goRefreshAccess() {
      return this.getAccessList({ host_id: this.host_id })
        .then((response) => {
          this.accesses = response.data;
          this.refreshChoice();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    tryCreate() {
      if (this.choice_user.id && this.choice_permissions) {
        this.createAccess({
          host_id: this.host_id,
          data: {
            user: this.choice_user.id,
            permissions: this.choice_permissions
          }
        })
          .then(() => {
            this.goRefreshAccess();
          })
          .catch((error) => {
            this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
          });
      }
    },
    tryUpdate(id, permissions) {
      console.log(id, permissions);
      if (id && permissions) {
        this.updateAccess({
          host_id: this.host_id,
          id: id,
          data: {
            permissions: permissions
          }
        })
          .then(() => {
            this.goRefreshAccess();
          })
          .catch((error) => {
            this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
          });
      }
    },
    tryDelete(id) {
      this.deleteAccess({
        host_id: this.host_id,
        id: id
      })
        .then(() => {
          this.goRefreshAccess();
        })
        .catch((error) => {
          this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
        });
    },
    tryRefreshUserList() {
      this.getUserList({
        params: { not_host_id: this.host_id }
      }).then((response) => {
        this.users = response.data;
      });
    },
    choiceUser(user) {
      this.choice_user = user;
    },
    refreshChoice() {
      this.choice_user = { username: "username" };
      this.choice_permissions = this.settings.default_permissions;
    }
  },
  mounted() {
    this.goRefreshAccess();
    this.refreshChoice();
  }
};
</script>
