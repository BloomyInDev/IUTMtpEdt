<script setup lang="ts">
import type { IAllData } from "~/utils/types";

const props = defineProps<{
    data: IAllData;
    weekNumber: number;
    showDate: boolean
}>();
//const dayString = computed(() =>
//    new Date(props.date.timeStart * 1000).toLocaleString("fr-FR", { weekday: "long", day: "numeric", month: "long" }),
//);
</script>
<template>
    <div>
        <p v-if="props.showDate">{{ new Date(props.data.day*1000).toLocaleString("fr-FR", { weekday: "long", day: "numeric", month: "long" }) }}</p>
        <div id="column">
            <EdtTile
                v-for="eventData in data.events"
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
</template>
<style>
#column {
    display: flex;
    flex-direction: column;
    gap: .25rem
}
p {
    text-align: center;
}
</style>
