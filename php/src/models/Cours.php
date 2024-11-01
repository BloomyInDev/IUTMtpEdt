<?php

class Cours extends Model {
    public function __construct() {
        $this->table = "Cours";
        $this->getConnection();
    }

    public function getAllInTimeOrder()
    {
        $sql = "SELECT * FROM ".$this->table." ORDER BY timeStart ASC";
        $query = $this->_connection->query($sql);
        return $query->fetch_all();
    }
}