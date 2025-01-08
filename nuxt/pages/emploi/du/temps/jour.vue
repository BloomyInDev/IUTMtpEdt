<script setup>
const week = ref(getDateWeek(new Date()));
const day = ref(new Date().getDay()-1);
const loading = ref(true);
const { data, refresh, status } = await useFetch(`/api/events/days`, {
    query: {
        week: week,
        groups: ["S4", "A1-Semestre-1", "S4b"].join(","),
    },
});
console.log(day.value)
const nextWeek = () => {
    day.value++;
    if (day.value > 6) {
        day.value = 0;
        week.value++;
    }
    refresh();
};
const prevWeek = () => {
    day.value--;
    if (day.value < 0) {
        day.value = 5;
        week.value--;
    }
    refresh();
};
const today = computed(()=>data.value.events.at(day.value))
</script>
<template>
    <div v-if="data == null">Il n'y a rien</div>
    <div v-else id="main">
        <div id="buttons">
            <button @click="prevWeek"><font-awesome icon="arrow-left" size="2x" /></button>
            <p>{{ new Date(today.day*1000).toLocaleString("fr-FR", { weekday: "long", day: "numeric", month: "long" })  }}</p>
            <button @click="nextWeek"><font-awesome icon="arrow-right" size="2x" /></button>
        </div>
        <div v-if="status == 'success'" id="day-planning">
            <EdtDay id="today-event" :key="today.id" :data="today" :date="new Date()" :show-date="false" />
        </div>
        <div v-else>
            <LoaderIcon />
        </div>
    </div>
</template>
<style>
div#main {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.5rem;
}
#day-planning {
    display: flex;
    justify-content: center;
    gap: 4px;
}
#day-planning > p {
    text-align: center;
}
#today-event {
   width: 90vw;
}

#buttons {
    display: flex;
    justify-content: space-between;
}
#buttons > button {
    background-color: transparent;
    border: 0;
    color: white;
}
</style>
