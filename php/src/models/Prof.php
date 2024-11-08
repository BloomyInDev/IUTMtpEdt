<?php

class Prof extends Model
{
    public function __construct()
    {
        $this->table = "Prof";
        $this->getConnection();
    }
}