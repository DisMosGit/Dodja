<template>
  <span>
    <h5>
      <b-badge :variant="status">
        {{ result.parameter }} {{ result.error }}
      </b-badge>
    </h5>
    {{ result.expected_value }}
    {{ result.comparison }}
    {{ result.obtained_value }}
  </span>
</template>

<script>
export default {
  name: "LogCheck",
  props: ["result"],
  computed: {
    status: function() {
      if (this.result.error) {
        return "danger";
      } else {
        if (this.result.check) {
          return "success";
        } else {
          return "warning";
        }
      }
    }
  }
};
</script>
