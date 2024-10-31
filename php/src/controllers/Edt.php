<?php
class Edt extends Controller
{
    /**
     * Show main page
     *
     * @return void
     */
    public function index()
    {
        
        $this->render("edt", []);
    }
    public function error()
    {
        $config = new Config();
        $this->render("404", ["config" => $config]);
    }
}
