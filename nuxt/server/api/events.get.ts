import type { IClasse, ICours, IProf } from "../mariadb-service";
import { db } from "../mariadb-service";

export default defineEventHandler(async (req) => {
    const urlParams = new URLSearchParams(req.path.slice(req.path.indexOf("?")));
    console.log(urlParams);
    const groups = urlParams.get("groups")?.split(",") || [];
    const startZone = urlParams.get("start") != null ? parseInt(urlParams.get("start") as string) : null;
    const endZone = urlParams.get("end") != null ? parseInt(urlParams.get("end") as string) : null;

    try {
        let eventResults;
        if (startZone !== null && endZone !== null) {
            [eventResults] = await db.execute<ICours[]>("SELECT * FROM Cours WHERE timeStart >= ? AND timeEnd <= ?", [
                startZone,
                endZone,
            ]);
        } else if (startZone !== null) {
            [eventResults] = await db.execute<ICours[]>("SELECT * FROM Cours WHERE timeStart >= ?", [startZone]);
        } else if (endZone !== null) {
            [eventResults] = await db.execute<ICours[]>("SELECT * FROM Cours WHERE timeEnd <= ?", [endZone]);
        } else {
            [eventResults] = await db.query<ICours[]>("SELECT * FROM Cours");
        }

        const eventData: IAllData[] = [];

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
            eventData.push({
                ...row,
                studentsGroups: studentsGroupsResult.map((v) => v.nom).sort(),
                profs: profsResults.map((v) => `${v.nom} ${v.prenom}`).sort(),
            });
        }
        if (groups.length > 0) {
            const filteredEventData = eventData.filter((event) =>
                groups.some((group) => event.studentsGroups.includes(group)),
            );
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
