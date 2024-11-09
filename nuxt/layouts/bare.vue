<script setup>
const color = useColorMode();
</script>

<template>
    <div class="min-h-screen bg-gray-800 text-white">
        <select v-model="$colorMode.preference">
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="sepia">Sepia</option>
        </select>

        <slot />
    </div>
</template>
