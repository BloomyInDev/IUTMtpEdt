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
    darkOrLight: computed(() => (tinycolor(props.color).darken(25).isDark() ? "tile dark" : "tile light")),
};
const profs = computed(() => props.profs.reduce((acc, cur, i) => `${acc}${i == 0 ? "" : " - "}${cur}`, ""));
const studentsGroups = computed(() =>
    props.studentsGroups.reduce((acc, cur, i) => `${acc}${i == 0 ? "" : " - "}${cur}`, ""),
);
</script>

<template>
    <div :class="colors.darkOrLight.value">
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
    display: flex;
    height: fit-content;
    width: 100%;
    align-items: center;
    gap: 0.5rem;
    overflow: hidden;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    line-height: 1.25rem;
    background-color: v-bind(colors.darker.value);
}
.tile > div {
    height: 100%;
    padding: 0.5rem;
}

.dark {
    color: white;
}
.light {
    color: black;
}

.date {
    display: flex;
    height: 18rem;
    flex-shrink: 0;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: v-bind(colors.normal.value);
}

.date > p {
    padding: 0;
}

.content {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.content > p:first-child {
    font-size: 1.125rem;
    line-height: 1.75rem;
    font-weight: bold;
}
.content > div {
    grid-template-columns: auto 1fr;
    place-items: center;
}
.content > div > p {
    width: 100%;
    text-wrap: wrap;
}
</style>
