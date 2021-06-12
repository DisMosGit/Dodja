<template>
  <textarea :id="editor_id"></textarea>
</template>

<script>
import yaml from "js-yaml";
import * as CodeMirror from "codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/eclipse.css";
import "codemirror/mode/python/python.js";
import "codemirror/mode/yaml/yaml.js";

export default {
  name: "ReadTextarea",
  props: ["default"],
  data() {
    return {
      text: "",
      editor: null,
      editor_id: "read-textarea-" + Math.random()
    };
  },

  methods: {
    addText(new_text) {
      this.editor.setValue(this.editor.getValue() + yaml.dump(new_text));
    },
    deleteText() {
      this.editor.setValue("");
    }
  },
  mounted() {
    this.editor = CodeMirror.fromTextArea(
      document.getElementById(this.editor_id),
      {
        theme: "eclipse",
        mode: "yaml",
        viewportMargin: 0,
        readOnly: true
      }
    );
    this.editor.setSize(null, "auto");
  },
  beforeDestroy() {
    delete this.editor;
  }
};
</script>
