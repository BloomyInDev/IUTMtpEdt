<?php
class Main extends Controller
{
    /**
     * Show main page
     *
     * @return void
     */
    public function index()
    {
        $this->render("index");
    }
    public function error()
    {
        $config = new Config();
        $this->render("404", ["config" => $config]);
    }
}
