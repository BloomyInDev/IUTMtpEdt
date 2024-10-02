from datetime import datetime, UTC

class Cours:
    def __init__(self) -> None:
        self.__nomCours:str = ""
        self.__salle:str = ""
        self.__classe:str = ""
        self.__heureDebut:str = ""
        self.__heureFin: str = ""
        pass

    def setNomCours(self,nomCours:str)-> None:
        self.__nomCours = nomCours
    def getNomCours(self):
        return self.__nomCours
    
    def setSalle(self,salle:str)-> None:
        self.__salle = salle
    def getSalle(self):
        return self.__salle
    
    def setClasse(self,classe:str)-> None:
        self.__classe = classe
    def getClasse(self):
        return self.__classe
    
    def setHeureDebut(self,heureDebut:str)-> None:
        self.__heureDebut = heureDebut
    def getHeureDebut(self):
        return self.__heureDebut
    
    def setHeureFin(self,heureFin:str)-> None:
        self.__heureFin = heureFin
    def getHeureFin(self):
        return self.__heureFin
    
