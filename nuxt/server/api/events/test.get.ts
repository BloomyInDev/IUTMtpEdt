import { getFirstDayOfWeek, getLastDayOfWeek } from "../../utils/days";

export default defineEventHandler(async (req) => {
    const today = new Date();
    return [getFirstDayOfWeek(today).toLocaleString("fr-FR"), getLastDayOfWeek(today).toLocaleString("fr-FR")];
});
