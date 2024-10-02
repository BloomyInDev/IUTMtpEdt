<?php
abstract class Controller
{
    public function render(string $file, array $data = [])
    {
        extract($data);
        ob_start();
        require_once ROOT . "views/" . strtolower(get_class($this)) . "/" . $file . ".php";
        $content = ob_get_clean();
        require_once ROOT . "views/layout/default.php";
    }
}
