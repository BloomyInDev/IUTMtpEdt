import type { RowDataPacket } from "mysql2/promise";
import { createPool } from "mysql2/promise";

export const db = createPool("mysql://root:ThisPasswordIsntSecure@localhost:3306/iutmtpedt");

export interface IClasse extends RowDataPacket {
    id: number;
    nom: string;
}

export interface IProf extends RowDataPacket {
    id: number;
    nom: string;
    prenom: string;
}

export interface ICours extends RowDataPacket {
    id: number;
    name: string;
    timeStart: number;
    timeEnd: number;
    place: string;
    color: string;
}

export interface IEnseigner extends RowDataPacket {
    idProf: number;
    idCours: number;
}

export interface IParticipants extends RowDataPacket {
    idProf: number;
    idCours: number;
}

export interface IDevoirs extends RowDataPacket {
    id: number;
    idCours: number;
    titre: string;
    description: string;
}

export interface IPieceJointe extends RowDataPacket {
    id: number;
    nom: string;
    fichier: Blob;
    idDevoir: number;
}
