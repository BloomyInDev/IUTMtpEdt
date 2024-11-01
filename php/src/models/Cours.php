<?php

class Cours extends Model {
    public function __construct() {
        $this->table = "Cours";
        $this->getConnection();
    }

    public function getAllWithDatas() {
        $sql = "SELECT * FROM ".$this->table."";
        $query = $this->_connection->query($sql);
        return $query->fetch_all();
    }
}