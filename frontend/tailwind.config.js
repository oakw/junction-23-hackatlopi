/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'gray-light': 'rgba(var(--color-gray-light), <alpha-value>)',
        'gray-dark': 'rgba(var(--color-gray-dark), <alpha-value>)',
      }
    },

  },
  plugins: [],
}

