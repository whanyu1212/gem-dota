import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";
import ReplayParserPanel from "./components/ReplayParserPanel.vue";
import "./style.css";

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component("ReplayParserPanel", ReplayParserPanel);
  },
} satisfies Theme;
