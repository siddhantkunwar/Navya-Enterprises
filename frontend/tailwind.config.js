/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
        extend: {
                borderRadius: {
                        lg: 'var(--radius)',
                        md: 'calc(var(--radius) - 2px)',
                        sm: 'calc(var(--radius) - 4px)'
                },
                colors: {
                        sage: '#AAB696',
                        olive: '#38443B',
                        brown: '#6B3F34',
                        forest: '#4B5D44',
                        background: 'hsl(var(--background))',
                        foreground: 'hsl(var(--foreground))',
                        card: {
                                DEFAULT: 'hsl(var(--card))',
                                foreground: 'hsl(var(--card-foreground))'
                        },
                        popover: {
                                DEFAULT: 'hsl(var(--popover))',
                                foreground: 'hsl(var(--popover-foreground))'
                        },
                        primary: {
                                DEFAULT: 'hsl(var(--primary))',
                                foreground: 'hsl(var(--primary-foreground))'
                        },
                        secondary: {
                                DEFAULT: 'hsl(var(--secondary))',
                                foreground: 'hsl(var(--secondary-foreground))'
                        },
                        muted: {
                                DEFAULT: 'hsl(var(--muted))',
                                foreground: 'hsl(var(--muted-foreground))'
                        },
                        accent: {
                                DEFAULT: 'hsl(var(--accent))',
                                foreground: 'hsl(var(--accent-foreground))'
                        },
                        destructive: {
                                DEFAULT: 'hsl(var(--destructive))',
                                foreground: 'hsl(var(--destructive-foreground))'
                        },
                        border: 'hsl(var(--border))',
                        input: 'hsl(var(--input))',
                        ring: 'hsl(var(--ring))',
                        chart: {
                                '1': 'hsl(var(--chart-1))',
                                '2': 'hsl(var(--chart-2))',
                                '3': 'hsl(var(--chart-3))',
                                '4': 'hsl(var(--chart-4))',
                                '5': 'hsl(var(--chart-5))'
                        }
                },
                fontFamily: {
                        heading: ['"Playfair Display"', 'serif'],
                        body: ['"Lato"', 'sans-serif'],
                },
                keyframes: {
                        'accordion-down': {
                                from: { height: '0' },
                                to: { height: 'var(--radix-accordion-content-height)' }
                        },
                        'accordion-up': {
                                from: { height: 'var(--radix-accordion-content-height)' },
                                to: { height: '0' }
                        },
                        'fade-in': {
                                from: { opacity: '0', transform: 'translateY(16px)' },
                                to: { opacity: '1', transform: 'translateY(0)' }
                        },
                        'slide-in-left': {
                                from: { opacity: '0', transform: 'translateX(-24px)' },
                                to: { opacity: '1', transform: 'translateX(0)' }
                        },
                        'slide-in-right': {
                                from: { opacity: '0', transform: 'translateX(24px)' },
                                to: { opacity: '1', transform: 'translateX(0)' }
                        }
                },
                animation: {
                        'accordion-down': 'accordion-down 0.2s ease-out',
                        'accordion-up': 'accordion-up 0.2s ease-out',
                        'fade-in': 'fade-in 0.6s ease-out forwards',
                        'slide-in-left': 'slide-in-left 0.6s ease-out forwards',
                        'slide-in-right': 'slide-in-right 0.6s ease-out forwards'
                }
        }
  },
  plugins: [require("tailwindcss-animate")],
};
