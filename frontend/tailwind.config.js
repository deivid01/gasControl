/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                gasBlue: '#2A4C96',
                gasBlueDark: '#1a3266',
                gasBlueLight: '#1AA8E8',
                gasBrandRed: '#E1040E',
            }
        },
    },
    plugins: [],
}
