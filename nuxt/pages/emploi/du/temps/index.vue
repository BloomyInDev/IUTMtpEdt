<script setup>
definePageMeta({
    layout: "bare",
});
const color = useColorMode()
console.log(color.value)
const { data } = await useFetch(`/api/events/days`, {
    query: {
        week: getDateWeek(new Date()),
        groups: ["S4", "A1-Semestre-1", "S4b"].join(","),
    },
});
console.log(data);
</script>
<template>
    <div class="flex flex-col gap-2 p-2">
        <div class="week-planning">
            <p>Lundi</p>
            <p>Mardi</p>
            <p>Mercredi</p>
            <p>Jeudi</p>
            <p>Vendredi</p>
            <p>Samedi</p>
            <div v-for="day in data.events" class="day-planning">
                <EdtTile
                    v-for="eventData in day"
                    :key="eventData.id"
                    :title="eventData.name"
                    :event-start="
                        new Date(eventData.timeStart * 1000).toLocaleTimeString('fr-FR', {
                            hour: '2-digit',
                            minute: '2-digit',
                        })
                    "
                    :event-end="
                        new Date(eventData.timeEnd * 1000).toLocaleTimeString('fr-FR', {
                            hour: '2-digit',
                            minute: '2-digit',
                        })
                    "
                    :profs="eventData.profs"
                    :students-groups="eventData.studentsGroups"
                    :place="eventData.place"
                    :color="eventData.color"
                />
            </div>
        </div>
        
    </div>
</template>
<style>
.week-planning {
    grid-template-columns: repeat(6, minmax(0, 1fr));
    @apply grid gap-1
}
.week-planning > p {
    @apply text-center
}

.day-planning {
    @apply flex gap-1 flex-col
}
</style>