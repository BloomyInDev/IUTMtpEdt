<script setup lang="ts">
import tinycolor from "tinycolor2";
const props = defineProps({
    title: { type: String, required: true },
    eventStart: { type: String, required: true },
    eventEnd: { type: String, required: true },
    profs: { type: Array<string>, default: [] },
    studentsGroups: { type: Array<string>, default: [] },
    color: {
        type: String,
        default: "#4d8eff",
        validator: (val) => {
            if (typeof val == "string") {
                const check = new RegExp(/^#([0-9a-f]{6}|[0-9a-f]{3})$/i);
                return check.test(val);
            } else {
                return false;
            }
        },
    },
});

const colors = {
    normal: computed(() => `background-color: ${props.color};`),
    brighter: computed(() => `background-color: ${tinycolor(props.color).brighten(25)};`),
    isDark: computed(() => tinycolor(props.color).isDark()),
};
</script>

<template>
    <div :class="colors.isDark ? 'tile dark' : 'tile light'" :style="colors.normal.value">
        <div class="date" :style="colors.brighter.value">
            <p class="font-bold">{{ props.eventStart }}</p>
            <p>{{ props.eventEnd }}</p>
        </div>
        <div class="content">
            <p>{{ props.title }}</p>

            <div v-if="props.profs.length > 0">
                <p v-for="(prof, i) in props.profs" :key="i">
                    {{ prof }}
                </p>
            </div>
            <div v-else>
                <p>Pas de professeurs</p>
            </div>

            <div v-if="props.studentsGroups.length > 0">
                <p v-for="(studentsGroup, i) in props.studentsGroups" :key="i">
                    {{ studentsGroup }}
                </p>
            </div>
            <div v-else>
                <p>Pas de groupes de classes</p>
            </div>
        </div>
    </div>
</template>

<style>
.tile {
    @apply flex h-24 w-full items-center gap-2 overflow-hidden rounded-lg;
}
.tile > div {
    @apply h-full p-2;
}

.dark {
    @apply text-white;
}
.light {
    @apply text-black;
}

.date {
    @apply flex flex-col items-center justify-center;
}
.date > p {
    @apply p-0;
}

.content {
    @apply flex flex-col justify-center;
}
.content > p:first-child {
    @apply text-xl font-bold;
}
</style>
