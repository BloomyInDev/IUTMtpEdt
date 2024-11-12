<script setup>
const { data } = await useFetch(`/api/events/days`, {
    query: {
        week: getDateWeek(new Date()),
        groups: ["S4", "A1-Semestre-1", "S4b"].join(","),
    },
});
</script>
<template>
    <div id="main">
        <div id="buttons"></div>
        <div id="week-planning">
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
div#main {
    display: flex;
    flex-direction: column;
    gap: .5rem;
    padding: 0.5rem;
}
#week-planning {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 4px;
}
#week-planning > p {
    text-align: center;
}

.day-planning {
    display: flex;
    gap: 4px;
    flex-direction: column;
}
</style>
