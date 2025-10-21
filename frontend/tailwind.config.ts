import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef2ff",
          100: "#e0e7ff",
          500: "#6366f1",
          600: "#4f46e5"
        },
        accent: {
          500: "#f97316"
        }
      },
      borderRadius: {
        xl: "0.75rem"
      }
    }
  },
  plugins: []
};

export default config;
