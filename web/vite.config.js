import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/500-AI-Agents-Projects/",
  plugins: [react()],
  server: {
    fs: {
      allow: [".."],
    },
  },
});
