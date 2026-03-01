/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./api/templates/**/*.html",
    "./api/static/js/**/*.js",
  ],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        grain: {
          paper: "#f8f4e9",
          soft: "#fffaf0",
          line: "#d7ccb1",
          ink: "#1d2b1f",
          muted: "#617363",
          field: "#3d7e50",
          deep: "#234f33",
          gold: "#d5a63e",
        },
      },
      fontFamily: {
        sans: ["Manrope", "sans-serif"],
        display: ["Space Grotesk", "sans-serif"],
      },
      boxShadow: {
        grain: "0 24px 48px rgba(26, 47, 31, 0.12)",
        card: "0 18px 40px rgba(31, 47, 33, 0.10)",
      },
      backgroundImage: {
        "grain-hero":
          "linear-gradient(135deg, rgba(17, 31, 20, 0.18), rgba(17, 31, 20, 0.42))",
      },
    },
  },
};
