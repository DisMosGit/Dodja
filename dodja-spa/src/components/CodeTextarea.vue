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
import "codemirror/mode/dockerfile/dockerfile.js";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/shell/shell.js";

export default {
  name: "CodeTextarea",
  props: {
    default: {
      type: String,
      default: "Yaml:\n\tkey: value"
    },
    mode: {
      type: String,
      default: "yaml"
    },
    is_read: {
      type: Boolean,
      default: false
    },
    height: {
      type: String,
      default: "auto"
    }
  },
  data() {
    return {
      editor: null,
      editor_id: "code-textarea-" + Math.random()
    };
  },
  computed: {
    text: {
      get: function() {
        switch (this.mode) {
          case "yaml":
            return yaml.load(this.editor.getValue());
          default:
            return this.editor.getValue();
        }
      },
      set: function(obj) {
        switch (this.mode) {
          case "yaml":
            if (typeof obj == "object") {
              this.editor.setValue(yaml.dump(obj));
            } else {
              this.editor.setValue(obj);
            }
            break;
          default:
            this.editor.setValue(obj);
            break;
        }
      }
    }
  },
  methods: {
    editText(value) {
      this.text = value;
    },
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
        lineNumbers: true,
        theme: "eclipse",
        mode: this.mode,
        viewportMargin: 3,
        readOnly: this.is_read
      }
    );
    this.editor.setValue(
      this.default.replace(/\\n/g, "\n").replace(/\\t/g, "    ")
    );
    this.editor.setSize(null, this.height);
  },
  beforeDestroy() {
    delete this.editor;
  }
};
</script>
