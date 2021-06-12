import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Login.vue")
  },
  {
    path: "/logout",
    name: "Logout",
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Login.vue")
  },
  {
    path: "/registration",
    name: "Registration",
    component: () =>
      import(/* webpackChunkName: "Registration" */ "../views/Registration.vue")
  },
  {
    path: "/profile",
    name: "Profile",
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Profile.vue")
  },
  {
    path: "/host",
    name: "HostList",
    component: () =>
      import(/* webpackChunkName: "HostList" */ "../views/HostList.vue")
  },
  {
    path: "/host/create",
    name: "HostCreate",
    component: () =>
      import(/* webpackChunkName: "HostCreate" */ "../views/HostCreate.vue")
  },
  {
    path: "/host/:id",
    name: "HostDetail",
    component: () =>
      import(/* webpackChunkName: "HostDetail" */ "../views/HostDetail.vue"),
    children: [
      // {
      //   path: "/host/:id/edit",
      //   name: "HostEdit",
      //   component: () =>
      //     import(/* webpackChunkName: "HostEdit" */ "../views/HostEdit.vue")
      // },
      {
        path: "/host/:id/monitoring",
        name: "HostMonitoring",
        component: () =>
          import(
            /* webpackChunkName: "HostMonitoring" */ "../views/HostMonitoring.vue"
          )
      },
      {
        path: "/host/:id/monitoring/:task",
        name: "HostMonitoringTask",
        component: () =>
          import(
            /* webpackChunkName: "HostMonitoringTask" */ "../views/HostMonitoringTask.vue"
          )
      },
      {
        path: "/host/:id/docker",
        name: "HostDocker",
        component: () =>
          import(
            /* webpackChunkName: "HostDocker" */ "../views/HostDocker.vue"
          ),
        children: [
          {
            path: "docker",
            name: "HostDockerInfo",
            component: () =>
              import(
                /* webpackChunkName: "HostDockerInfo" */ "../views/docker/HostDockerInfo.vue"
              )
          },
          {
            path: "container",
            name: "HostContainerList",
            component: () =>
              import(
                /* webpackChunkName: "HostContainerList" */ "../views/docker/HostContainerList.vue"
              )
          },
          {
            path: "container/:obj",
            name: "HostContainerDetail",
            component: () =>
              import(
                /* webpackChunkName: "HostContainerDetail" */ "../views/docker/HostContainerDetail.vue"
              )
          },
          {
            path: "image",
            name: "HostImageList",
            component: () =>
              import(
                /* webpackChunkName: "HostImageList" */ "../views/docker/HostImageList.vue"
              )
          },
          {
            path: "image/:obj",
            name: "HostImageDetail",
            component: () =>
              import(
                /* webpackChunkName: "HostImageDetail" */ "../views/docker/HostImageDetail.vue"
              )
          },
          {
            path: "volume",
            name: "HostVolumeList",
            component: () =>
              import(
                /* webpackChunkName: "HostVolumeList" */ "../views/docker/HostVolumeList.vue"
              )
          },
          {
            path: "volume/:obj",
            name: "HostVolumeDetail",
            component: () =>
              import(
                /* webpackChunkName: "HostVolumeDetail" */ "../views/docker/HostVolumeDetail.vue"
              )
          },
          {
            path: "network",
            name: "HostNetworkList",
            component: () =>
              import(
                /* webpackChunkName: "HostNetworkList" */ "../views/docker/HostNetworkList.vue"
              )
          },
          {
            path: "network/:obj",
            name: "HostNetworkDetail",
            component: () =>
              import(
                /* webpackChunkName: "HostNetworkDetail" */ "../views/docker/HostNetworkDetail.vue"
              )
          }
        ]
      }
    ]
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
