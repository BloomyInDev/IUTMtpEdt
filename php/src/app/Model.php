<?php
abstract class Model
{
    private $host = "database";
    private $db_name = "iutmtpedt";
    private $username = "username";
    private $password = "password";

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
            $this->_connection = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
            $this->_connection->exec("set names utf8");
            $this->_connection->exec("USE " . $this->db_name);
        } catch (Exception $exception) {
            echo "Connection error : " . $exception->getMessage();
        }
    }

    /**
     * Get one row in a table with an id
     *
     * @return void
     */
    public function getOne()
    {
        $sql = "SELECT * FROM :table WHERE id=:id";
        $query = $this->_connection->prepare($sql);
        $query->bindParam(":table", $this->table);
        $query->bindParam(":id", $this->id);
        $query->execute();
        return $query->fetch();
    }

    /**
     * Get all row in a table
     */
    public function getAll()
    {
        $sql = "SELECT * FROM " . $this->table;
        $query = $this->_connection->prepare($sql);
        $query->execute();
        return $query->fetch();
    }
}
