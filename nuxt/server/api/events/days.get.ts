import type { IClasse, ICours, IProf } from "../../utils/mariadb-service";
import { db } from "../../utils/mariadb-service";
import { getDateWeek, getFirstDayOfWeek, getLastDayOfWeek } from "../../utils/days";

export default defineEventHandler(async (req) => {
    const urlParams = new URLSearchParams(req.path.slice(req.path.indexOf("?")));
    console.log(urlParams);
    const groups = urlParams.get("groups")?.split(",") || [];
    const place = urlParams.get("place")
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
        let sql:string, args:unknown[]
        if (place !== null) {
            sql = "SELECT * FROM Cours WHERE timeStart >= ? AND timeEnd <= ? AND place LIKE ? ORDER BY timeStart ASC"
            args = [Math.round(startZone.getTime() / 1000),
                Math.round(endZone.getTime() / 1000),`%${place}%`]
        } else {
            sql = "SELECT * FROM Cours WHERE timeStart >= ? AND timeEnd <= ? ORDER BY timeStart ASC"
            args = [
                Math.round(startZone.getTime() / 1000),
                Math.round(endZone.getTime() / 1000),
            ]
        }
        const [eventResults] = await db.execute<ICours[]>(sql, args);

        const eventData: IData[][] = [[], [], [], [], [], []];

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
            const filteredEventData: IAllData[] = [];
            for (let i = 0; i < eventData.length; i++) {
                filteredEventData.push({day:0, events:[]});
                const day = eventData[i];
                for (let j = 0; j < day.length; j++) {
                    const event = day[j];
                    if (groups.some((group) => event.studentsGroups.includes(group))) {
                        filteredEventData[i].events.push(event);
                    }
                }
                if (filteredEventData[i].events.length > 0) {
                    filteredEventData[i].day = filteredEventData[i].events[0].timeStart;
                } else if (i>0) {
                    filteredEventData[i].day = Math.round(new Date((filteredEventData[i-1].day*1000) + (24 * 60 * 60 * 1000)).getTime()/1000)
                } else {
                    filteredEventData[i].day = Math.round(startZone.getTime()/1000)
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

interface IAllData {
    day: number;
    events: IData[];
}
interface IData extends ICours {
    studentsGroups: string[];
    profs: string[];
}
