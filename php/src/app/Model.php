<?php
abstract class Model
{
    private $host = "database";
    private $db_name = "iutmtpedt";
    private $username = "root";
    private $password = "ThisPasswordIsntSecure";

    protected $_connection;

    public $table;
    public $id;

    /**
     * Initialise the database
     *
     * @return void
     */
    public function getConnection()
    {
        // Remove old connection
        $this->_connection = null;

        try {
            $this->_connection = new mysqli($this->host, $this->username, $this->password, $this->db_name);
            $this->_connection->query("set names utf8");
            $this->_connection->query("USE " . $this->db_name);
        } catch (Exception $exception) {
            echo "Connection error : " . $exception->getMessage();
        }
    }

    /**
     * Get one row in a table with an id
     *
     * @return void
     */
    public function getOne(int $id)
    {
        $sql = "SELECT * FROM ".$this->table." WHERE id=".$id;
        $query = $this->_connection->query($sql);
        return $query->fetch_all();
    }

    /**
     * Get all row in a table
     */
    public function getAll()
    {
        $sql = "SELECT * FROM ".$this->table;
        $query = $this->_connection->query($sql);
        return $query->fetch_all();
    }
}
