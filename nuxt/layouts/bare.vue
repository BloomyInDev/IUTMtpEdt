<script setup>
const color = useColorMode();
</script>

<template>
    <div>
        <slot/>
    </div>
</template>

<style>
div {
    min-height: 100vh;
    background-color: gray;
    color: white;
}
</style>