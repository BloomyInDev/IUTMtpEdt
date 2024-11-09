<script setup lang="ts">
import tinycolor from "tinycolor2";
const props = defineProps({
    title: { type: String, required: true },
    eventStart: { type: String, required: true },
    eventEnd: { type: String, required: true },
    profs: { type: Array<string>, default: [] },
    studentsGroups: { type: Array<string>, default: [] },
    place: { type: String, required: true },
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
    normal: computed(() => props.color),
    brighter: computed(() => tinycolor(props.color).brighten(25)),
    darker: computed(() => tinycolor(props.color).darken(25)),
    isDark: computed(() => tinycolor(props.color).isDark()),
};
const profs = computed(() => props.profs.reduce((acc, cur, i) => `${acc}${i == 0 ? "" : " - "}${cur}`, ""));
const studentsGroups = computed(() =>
    props.studentsGroups.reduce((acc, cur, i) => `${acc}${i == 0 ? "" : " - "}${cur}`, ""),
);
</script>

<template>
    <div :class="colors.isDark ? 'tile dark' : 'tile light'">
        <div class="date">
            <p class="font-bold">{{ props.eventStart }}</p>
            <p>{{ props.eventEnd }}</p>
        </div>
        <div class="content">
            <p>{{ props.title }}</p>

            <div class="grid grid-cols-2 items-center justify-start gap-2 p-1">
                <font-awesome
                    v-if="profs.length == 0 || (profs.length > 0 && profs.split('-').length < 2)"
                    icon="user"
                />
                <font-awesome v-else icon="users" />
                <p v-if="profs.length > 0">{{ profs }}</p>
                <p v-else>Pas de professeurs</p>
                <font-awesome icon="graduation-cap" />
                <p v-if="studentsGroups.length > 0">{{ studentsGroups }}</p>
                <p v-else>Pas de groupes de classes</p>
                <font-awesome icon="location-dot" />
                <p>{{ props.place }}</p>
            </div>
        </div>
    </div>
</template>

<style>
.tile {
    background-color: v-bind(colors.normal.value);
    @apply flex h-fit w-full items-center gap-2 overflow-hidden rounded-lg text-sm;
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
    background-color: v-bind(colors.brighter.value);
    @apply flex h-72 w-16 flex-shrink-0 flex-col items-center justify-center;
}

.date > p {
    @apply p-0;
}

.content {
    @apply flex flex-col justify-center;
}
.content > p:first-child {
    @apply text-lg font-bold;
}
.content > div {
    grid-template-columns: auto 1fr;
    @apply place-items-center;
}
.content > div > p {
    @apply w-full text-wrap;
}

@media (prefers-color-scheme: dark) {
    .tile {
        background-color: v-bind(colors.darker.value);
    }

    .date {
        background-color: v-bind(colors.normal.value);
    }
}
</style>
