
 /** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./events/templates/**/*.html",
    "./events/**/*.py", // optional, sometimes used in inline styles
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
