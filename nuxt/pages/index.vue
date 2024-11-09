<script setup lang="ts">
const data = await useFetch("/api/events?groups=S4");
</script>
<template>
    <div>
        <div>coucou</div>
        <div>{{ data }}</div>
    </div>
</template>
