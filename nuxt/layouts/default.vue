<template>
    <div class="layout grid min-h-screen">
        <header class="flex w-full items-center justify-between bg-gray-500 p-2 pr-3">
            <h1 class="text-2xl font-bold">IUT-Mtp-edt</h1>
            <nav class="flex items-center justify-center gap-2">
                <nuxt-link to="/"><font-awesome icon="house" size="lg" /></nuxt-link>
                <nuxt-link to="/emploi/du/temps"><font-awesome icon="calendar" size="lg" /></nuxt-link>
            </nav>
        </header>
        <slot />
        <footer class="flex w-full bg-gray-500 p-2">
            <p class="text-center">Site créé avec ❤️ pour vous.</p>
        </footer>
    </div>
</template>
<style>
.layout {
    grid-template-rows: auto 1fr auto;
}
</style>
