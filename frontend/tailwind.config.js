/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                gasBlue: '#1D4ED8',
                gasNacional: '#F59E0B',
            }
        },
    },
    plugins: [],
}
