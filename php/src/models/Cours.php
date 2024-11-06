<?php

class Cours extends Model {
    public function __construct() {
        $this->table = "Cours";
        $this->getConnection();
        $this->table_link_prof = "Enseigner";
        $this->table_link_classe = "Participants";
    }

    public function getProfIdOfCours(int $id) {
        $sql = "SELECT idProf FROM ".$this->table_link_prof." WHERE idCours = ".$id;
        $query = $this->_connection->query($sql);
        $result = [];
        foreach ($query->fetch_all() as $i => $value) {
            $result[$i]=$value[0];
        }
        return $result;
    }

    public function getClasseIdOfCours(int $id) {
        $sql = "SELECT idClasse FROM ".$this->table_link_classe." WHERE idCours = ".$id;
        $query = $this->_connection->query($sql);
        $result = [];
        foreach ($query->fetch_all() as $i => $value) {
            $result[$i]=$value[0];
        }
        return $result;
    }

    public function getAllInTimeOrder()
    {
        $sql = "SELECT * FROM ".$this->table." ORDER BY timeStart ASC";
        $query = $this->_connection->query($sql);
        return $query->fetch_all();
    }
}