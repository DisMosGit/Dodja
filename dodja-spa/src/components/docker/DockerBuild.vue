<template>
  <span class="h3 mx-2 align-middle" v-if="version">
    <span class="badge badge-light">{{ version.Version }}</span>
    <span class="badge badge-light">{{ version.Arch }}</span>
    <span class="badge badge-light">{{ version.Os }}</span>
    <!-- <p>
      Docker Info: {{ info.Containers }}
      {{ info.ContainersPaused }}
      {{ info.ContainersRunning }}
      {{ info.ContainersStopped }}
      {{ info.Images }}
      {{ info.MemTotal }}
      {{ info.OSType }}
      {{ info.ServerVersion }}
    </p> -->
  </span>
</template>

<script>
export default {
  name: "DockerBuild",
  props: ["info", "version"]
};
</script>
