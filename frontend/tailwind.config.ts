/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Fraunces'", "Georgia", "serif"],
        body: ["'DM Sans'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        navy: {
          950: "#070d1a",
          900: "#0b1424",
          800: "#101e36",
          700: "#162844",
          600: "#1e3658",
        },
        accent: {
          DEFAULT: "#4ade80",
          dim: "#22c55e",
          glow: "rgba(74,222,128,0.15)",
        },
        surface: {
          DEFAULT: "#111827",
          raised: "#1a2535",
          border: "rgba(255,255,255,0.07)",
        },
      },
      animation: {
        "fade-up": "fadeUp 0.5s ease forwards",
        "pulse-glow": "pulseGlow 2s ease-in-out infinite",
        "spin-slow": "spin 3s linear infinite",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseGlow: {
          "0%,100%": { boxShadow: "0 0 0 0 rgba(74,222,128,0)" },
          "50%": { boxShadow: "0 0 20px 4px rgba(74,222,128,0.2)" },
        },
      },
    },
  },
  plugins: [],
};
