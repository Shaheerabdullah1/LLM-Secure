/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'chat-bg': '#ffffff',
        'user-bubble': '#e5e7eb',
        'bot-bubble': '#f3f4f6',
      }
    },
  },
  plugins: [],
} 