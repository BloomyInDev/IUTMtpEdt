<template>
    <div class="layout grid min-h-screen">
        <header>
            <h1>IUT-Mtp-edt</h1>
            <nav>
                <nuxt-link to="/"><font-awesome icon="house" size="lg" /></nuxt-link>
                <nuxt-link to="/emploi/du/temps"><font-awesome icon="calendar" size="lg" /></nuxt-link>
            </nav>
        </header>
        <main>
            <slot />
        </main>
        <footer>
            <p>Site créé avec ❤️ pour vous.</p>
        </footer>
    </div>
</template>
<style>
.layout {
    display: grid;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
}
header {
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
    padding: 0.5rem;
    padding-right: 0.25rem;
    background-color: #374141;
}
header > h1 {
    font-size: 1.5rem;
    line-height: 2rem;
    font-weight: bold;
    color: white;
}
header > nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
}

main {
    background-color: #4b5555;
    color: white;
}

footer {
    display: flex;
    width: 100%;
    background-color: #374141;
    padding: 0.5rem;
    text-align: center;
}
</style>
