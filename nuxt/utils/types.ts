export interface IClasse {
    id: number;
    nom: string;
}

export interface IProf {
    id: number;
    nom: string;
    prenom: string;
}

export interface ICours {
    id: number;
    name: string;
    timeStart: number;
    timeEnd: number;
    place: string;
    color: string;
}

export interface IEnseigner {
    idProf: number;
    idCours: number;
}

export interface IParticipants {
    idProf: number;
    idCours: number;
}

export interface IDevoirs {
    id: number;
    idCours: number;
    titre: string;
    description: string;
}

export interface IPieceJointe {
    id: number;
    nom: string;
    fichier: Blob;
    idDevoir: number;
}

export interface IAllData {
    day: number;
    events: ICoursWithLinkedPersons[];
}

export interface ICoursWithLinkedPersons extends ICours {
    studentsGroups: string[];
    profs: string[];
}
