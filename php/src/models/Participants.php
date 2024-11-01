<?php

class Participants extends Model {
    public function __construct() {
        $this->table = "Participants";
        $this->getConnection();
    }
    public function getClasseIdOfCours(int $id) {
        $sql = "SELECT idClasse FROM ".$this->table." WHERE idCours = ".$id;
        $query = $this->_connection->query($sql);
        $result = [];
        foreach ($query->fetch_all() as $i => $value) {
            $result[$i]=$value[0];
        }
        return $result;
    }
}