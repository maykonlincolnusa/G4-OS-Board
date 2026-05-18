import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#f2f5f8",
        panel: "#ffffff",
        ink: "#0f172a",
        muted: "#64748b",
        line: "#dbe2ea",
        accent: "#0f766e",
        danger: "#b91c1c",
        warning: "#b45309"
      },
      fontFamily: {
        sans: ["Manrope", "Segoe UI", "sans-serif"]
      }
    }
  },
  plugins: []
};

export default config;

