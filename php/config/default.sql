CREATE DATABASE iutmtpedt;

USE iutmtpedt;

CREATE TABLE Classe (
    id INT AUTO_INCREMENT,
    nom TINYTEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Prof (
    id INT AUTO_INCREMENT,
    nom TINYTEXT NOT NULL,
    prenom TINYTEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Cours (
    id INT AUTO_INCREMENT,
    name TINYTEXT NOT NULL,
    timeStart INT8 NOT NULL,
    timeEnd INT8 NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Enseigner (
    idProf INT,
    idCours INT,
    PRIMARY KEY(idProf, idCours),
    CONSTRAINT enseignerProfReference FOREIGN KEY(idProf) REFERENCES Prof(id),
    CONSTRAINT enseignerCoursReference FOREIGN KEY(idCours) REFERENCES Cours(id)
);

CREATE TABLE Participants (
    idClasse INT,
    idCours INT,
    PRIMARY KEY(idClasse, idCours),
    CONSTRAINT participantsClasseReference FOREIGN KEY(idClasse) REFERENCES Classe(id),
    CONSTRAINT participantsCoursReference FOREIGN KEY(idCours) REFERENCES Cours(id)
);

CREATE TABLE Devoirs (
    id INT,
    idCours INT,
    titre TINYTEXT NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT devoirsCoursReference FOREIGN KEY(idCours) REFERENCES Cours(id)
);

CREATE TABLE PieceJointe (
    id INT,
    nom TINYTEXT NOT NULL,
    fichier LONGBLOB NOT NULL,
    idDevoir INT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT pieceJointeDevoirReference FOREIGN KEY(idDevoir) REFERENCES Devoirs(id)
);