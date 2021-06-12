<template>
  <b-row class="my-1">
    <b-col cols="7" class="px-1">
      <b-form-input v-model="access.user.username" disabled></b-form-input>
    </b-col>
    <b-col cols="3" class="px-1">
      <b-form-input
        placeholder="permissions"
        v-model="access.permissions"
      ></b-form-input>
    </b-col>
    <b-col cols="2" class="px-1">
      <b-button-group>
        <b-button
          variant="warning"
          v-on:click="$emit('updateMe', access.id, access.permissions)"
        >
          <b-icon-pencil></b-icon-pencil>
        </b-button>
        <b-button variant="danger" v-on:click="$emit('deleteMe', access.id)">
          <b-icon-trash></b-icon-trash>
        </b-button>
      </b-button-group>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "AccessConfig",
  model: {
    prop: "access",
    event: "change"
  },
  props: {
    access: Object
  },
  data() {
    return {
      permissions: this.access.permissions
    };
  }
};
</script>
