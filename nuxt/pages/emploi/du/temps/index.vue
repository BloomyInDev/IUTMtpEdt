<script setup>
const today = new Date()
today.setHours(0,0,0)
const start = Math.round(today.getTime() / 1000);
today.setHours(23,59,59)
const end = Math.round(today.getTime() / 1000);
const {data} = await useFetch(`/api/events`, {
    query: {
        start: start,
        end: end
    },
});
console.log(data.value.events);
//const data = { start: ref(new Date().toLocaleTimeString("fr-FR",{hour:"2-digit",minute:"2-digit"})), end: ref(new Date().toLocaleTimeString("fr-FR",{hour:"2-digit",minute:"2-digit"})) };
</script>
<template>
    <div class="p-8">
        <!--<EdtTile title="Cours" :event-start="data.start" :event-end="data.end" color="#0000ff" />-->
        <div v-for="event in data.events">
            <EdtTile
                :title="event.name"
                :event-start="
                    new Date(event.timeStart*1000).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
                "
                :event-end="
                    new Date(event.timeEnd*1000).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
                "
                :profs="event.profs"
            />
        </div>
    </div>
</template>
