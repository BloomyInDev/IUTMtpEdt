// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    devtools: { enabled: true },
    ssr:false,
    modules: ["@nuxt/eslint", "@nuxtjs/tailwindcss", "@vesp/nuxt-fontawesome"],
    typescript: {
        typeCheck: true,
    },
    fontawesome: {
        icons: {
            solid: ["house", "calendar"],
        },
    },
});