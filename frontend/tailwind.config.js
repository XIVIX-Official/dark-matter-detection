export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#030712',
        }
      },
      animation: {
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        fadeIn: 'fadeIn 0.3s ease-in',
      },
      keyframes: {
        fadeIn: {
          'from': { opacity: '0' },
          'to': { opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}