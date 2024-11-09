import type { IClasse, ICours, IProf } from "../../utils/mariadb-service";
import { db } from "../../utils/mariadb-service";
import { getDateWeek, getFirstDayOfWeek, getLastDayOfWeek } from "../../utils/days";

export default defineEventHandler(async (req) => {
    const urlParams = new URLSearchParams(req.path.slice(req.path.indexOf("?")));
    console.log(urlParams);
    const groups = urlParams.get("groups")?.split(",") || [];
    const week = urlParams.get("week") != null ? parseInt(urlParams.get("week") as string) : null;
    if (week == null) {
        throw createError({
            statusCode: 400,
            statusMessage: "You must specify a week",
        });
    }
    let date = new Date();
    date.setHours(0, 0, 0);
    while (week != getDateWeek(date)) {
        if (week < getDateWeek(date)) {
            date = new Date(date.getTime() - 7 * 24 * 60 * 60 * 1000);
        } else {
            date = new Date(date.getTime() + 7 * 24 * 60 * 60 * 1000);
        }
    }
    const startZone = getFirstDayOfWeek(date);
    const endZone = getLastDayOfWeek(date);
    console.log(startZone, endZone, startZone.getTime() < endZone.getTime());
    try {
        const [eventResults] = await db.execute<ICours[]>("SELECT * FROM Cours WHERE timeStart >= ? AND timeEnd <= ? ORDER BY timeStart ASC", [
            Math.round(startZone.getTime() / 1000),
            Math.round(endZone.getTime() / 1000),
        ]);

        const eventData: IAllData[][] = [[], [], [], [], [], [], []];

        for (let index = 0; index < eventResults.length; index++) {
            const row = eventResults[index];
            const [studentsGroupsResult] = await db.execute<IClasse[]>(
                "SELECT nom FROM Participants p JOIN Classe c ON p.idClasse = c.id WHERE p.idCours = ?",
                [row.id],
            );
            const [profsResults] = await db.execute<IProf[]>(
                "SELECT nom, prenom FROM Enseigner e JOIN Prof p ON e.idProf = p.id WHERE e.idCours = ?",
                [row.id],
            );
            const dayOfWeek = new Date(row.timeStart * 1000).getDay() - 1;
            eventData[dayOfWeek].push({
                ...row,
                studentsGroups: studentsGroupsResult.map((v) => v.nom).sort(),
                profs: profsResults.map((v) => `${v.nom} ${v.prenom}`).sort(),
            });
        }
        if (groups.length > 0) {
            const filteredEventData: IAllData[][] = [];
            for (let i = 0; i < eventData.length; i++) {
                filteredEventData.push([]);
                const day = eventData[i];
                for (let j = 0; j < day.length; j++) {
                    const event = day[j];
                    if (groups.some((group) => event.studentsGroups.includes(group))) {
                        filteredEventData[i].push(event);
                    }
                }
            }
            return { events: filteredEventData };
        } else {
            return { events: eventData };
        }
    } catch (e) {
        throw createError({
            statusCode: 400,
            statusMessage: "Error fetching events",
        });
    }
});

interface IAllData extends ICours {
    studentsGroups: string[];
    profs: string[];
}
