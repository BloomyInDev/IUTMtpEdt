<?php

class Enseigner extends Model {
    public function __construct() {
        $this->table = "Enseigner";
        $this->getConnection();
    }
    public function getProfIdOfCours(int $id) {
        $sql = "SELECT idProf FROM ".$this->table." WHERE idCours = ".$id;
        $query = $this->_connection->query($sql);
        $result = [];
        foreach ($query->fetch_all() as $i => $value) {
            $result[$i]=$value[0];
        }
        return $result;
    }
}