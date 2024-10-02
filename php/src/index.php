<?php
// const "ROOT" at root
define("ROOT", str_replace("index.php", "", $_SERVER["SCRIPT_FILENAME"]));

require_once ROOT . "app/Model.php";
require_once ROOT . "app/Controller.php";
require_once ROOT . "app/Config.php";

if (array_key_exists("p", $_GET)) {
    $param_raw = $_GET["p"];
} else {
    $param_raw = "/";
}
$params = explode("/", $param_raw);

array_shift($params);
session_start();
if ($params[0] != "") {
    $controller = ucfirst($params[0]);
    $action = isset($params[1]) ? $params[1] : "index";
    if (@include_once ROOT . "controllers/" . $controller . ".php") {
        $controller = new $controller();
        if (method_exists($controller, $action)) {
            $controller->$action();
        } else {
            http_response_code(404);
            require_once ROOT . "controllers/Main.php";
            $controller = new Main();
            $controller->error();
        }
    } else {
        http_response_code(404);
        require_once ROOT . "controllers/Main.php";
        $controller = new Main();
        $controller->error();
    }
} else {
    // No specific path asked, going to Main page
    require_once ROOT . "controllers/Main.php";
    $controller = new Main();
    $controller->index();
}
