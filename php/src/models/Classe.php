<?php

class Classe extends Model {
    public function __construct() {
        $this->table = "Classe";
        $this->getConnection();
    }
}