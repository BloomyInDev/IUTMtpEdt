<script setup lang="ts">
const data = await useFetch("/api/events?groups=S4");
</script>
<template>
    <div id="home">
        <div>coucou</div>
        <LoaderIcon/>
    </div>
</template>
<style>
div#home {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}
</style>