<template>
  <div id="app">
    <b-navbar toggleable="md" variant="dark" type="dark" z-index="10">
      <!-- <b-navbar-brand>Dodja</b-navbar-brand> -->

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item
            :to="{ name: 'HostList' }"
            exact
            exact-active-class="active"
          >
            {{ $t("list") | capitalize }}
          </b-nav-item>
          <b-nav-item disabled>
            |
          </b-nav-item>
          <b-nav-item
            v-if="host_id"
            :to="{ name: 'HostDetail' }"
            exact
            exact-active-class="active"
          >
            {{ $t("detail") | capitalize }}
          </b-nav-item>
          <b-nav-item
            v-if="host_id"
            :to="{ name: 'HostMonitoring' }"
            exact
            exact-active-class="active"
          >
            {{ $t("monitoring") | capitalize }}
          </b-nav-item>
          <b-nav-item
            v-if="host_id"
            :to="{ name: 'HostDocker' }"
            exact
            exact-active-class="active"
          >
            {{ $t("docker") | capitalize }}
          </b-nav-item>
          <b-nav-item v-if="host_id" v-b-toggle.sidebar-right>
            {{ $tc("note", 2) | capitalize }}
          </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-form class="mx-2">
            <b-form-select
              v-model="$i18n.locale"
              :options="options"
              size="sm"
            ></b-form-select>
          </b-nav-form>
          <b-nav-item
            v-if="auth"
            :to="{ name: 'Profile' }"
            exact
            exact-active-class="active"
          >
            <em>{{ user.username }}</em>
          </b-nav-item>
          <b-nav-item
            v-show="auth"
            :to="{ name: 'Logout' }"
            exact
            exact-active-class="active"
          >
            {{ $t("logout") | capitalize }}
          </b-nav-item>
          <b-nav-item
            v-show="!auth"
            :to="{ name: 'Login' }"
            exact
            exact-active-class="active"
          >
            {{ $t("login") | capitalize }}
          </b-nav-item>
          <b-nav-item
            v-show="!auth"
            :to="{ name: 'Registration' }"
            exact
            exact-active-class="active"
          >
            {{ $t("registration") | capitalize }}
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-alert hide>{{ this.message }}</b-alert>
    <div>
      <SidebarLeft></SidebarLeft>
      <SidebarRight></SidebarRight>
      <b-container fluid="md">
        <router-view />
      </b-container>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";

import SidebarLeft from "@/views/SidebarLeft";
import SidebarRight from "@/views/SidebarRight";

export default {
  name: "App",
  components: {
    SidebarLeft,
    SidebarRight
  },
  data() {
    return {
      interval: null,
      menuVisible: false,
      notification: null,
      options: [
        { value: "en", text: "EN" },
        { value: "ru", text: "РУС" }
      ]
    };
  },
  mounted() {
    console.log("auth:", this.auth);
    this.checkSession();
    this.interval = setInterval(() => {
      this.checkSession();
    }, 1000 * 1 * 5);
  },
  computed: {
    ...mapGetters(["user", "auth", "message", "last_refresh"]),
    host_id: function() {
      return this.$route.params.id;
    }
  },
  methods: {
    ...mapActions(["logout", "refreshToken"]),
    ...mapMutations(["setMsg"]),
    checkSession() {
      if (
        this.auth &&
        new Date(this.last_refresh.getTime() + 60000 * 15) <= new Date()
      ) {
        this.refreshToken();
      }
    },
    notifyMe: function(title, text) {
      if (!("Notification" in window)) {
        alert("This browser does not support desktop notification");
      } else if (Notification.permission === "granted") {
        this.notification = new Notification(title, {
          body: text,
          icon: "http://localhost:8000/static/favicon.ico"
        });
      } else if (Notification.permission !== "denied") {
        Notification.requestPermission(function(permission) {
          if (permission === "granted") {
            this.notification = new Notification(title, {
              body: text,
              icon: "http://localhost:8000/static/favicon.ico"
            });
          }
        });
      }
    }
  },
  beforeDestroy() {
    clearInterval(this.interval);
  }
};
</script>

<style lang="scss">
#app {
  width: 100%;
  height: 100%;
}
#sidebar-left,
#sidebar-right {
  top: 5rem;
}
</style>
