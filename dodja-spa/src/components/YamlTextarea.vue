<template>
  <textarea :id="editor_id"></textarea>
  <!-- <b-button variant="warning" v-on:click="yamlParse()">
      Save text
    </b-button> -->
</template>

<script>
import yaml from "js-yaml";
import * as CodeMirror from "codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/eclipse.css";
import "codemirror/mode/yaml/yaml.js";
import "codemirror/mode/javascript/javascript.js";

export default {
  name: "ReadTextarea",
  props: ["default"],
  data() {
    return {
      editor: null,
      editor_id: "yaml-textarea-" + Math.random()
    };
  },
  computed: {
    text: {
      get: function() {
        return yaml.load(this.editor.getValue());
      },
      set: function(obj) {
        if (typeof obj == "object") {
          this.editor.setValue(yaml.dump(obj));
        } else {
          this.editor.setValue(obj);
        }
      }
    }
  },
  methods: {
    editText(value) {
      this.text = value;
    }
  },
  mounted() {
    this.editor = CodeMirror.fromTextArea(
      document.getElementById(this.editor_id),
      {
        lineNumbers: true,
        theme: "eclipse",
        mode: "yaml",
        viewportMargin: 3
      }
    );
    if (this.default) {
      this.editor.setValue(
        this.default.replace("\\n", "\n").replace("\\t", "    ")
      );
    } else {
      this.editor.setValue("Yaml:\n  - key: value");
    }
    this.editor.setSize(null, 110);
  },
  beforeDestroy() {
    delete this.editor;
  }
};
</script>
