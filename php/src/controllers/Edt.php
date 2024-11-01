<?php
require_once(ROOT."models/Cours.php");
require_once(ROOT."models/Enseigner.php");
require_once(ROOT."models/Participants.php");
require_once(ROOT."models/Prof.php");
require_once(ROOT."models/Classe.php");
class Edt extends Controller
{
    /**
     * Show main page
     *
     * @return void
     */
    public function index()
    {
        $this->render("edt", ["cours"=>$this->getCleanCours()]);
    }
    public function raw()
    {
        $this->render("raw", ["cours"=>$this->getCleanCours()]);
    }
    protected function getCleanCours()
    {
        $cours = new Cours();
        $enseigner = new Enseigner();
        $participants = new Participants();
        $prof = new Prof();
        $classe = new Classe();
        $cours_data = [];
        foreach ($cours->getAll() as $i => $data) {
            $cours_data[$i] = ["id"=>$data[0],"nom"=>$data[1],"timestampStart"=>$data[2],"timestampEnd"=>$data[3]];
            $cours_data[$i]["raw_profs"] = $enseigner->getProfIdOfCours($data[0]);
            $cours_data[$i]["raw_classes"] = $participants->getClasseIdOfCours($data[0]);
            $cours_data[$i]["profs"] = [];
            $cours_data[$i]["classes"] = [];
            foreach ($cours_data[$i]["raw_profs"] as $k => $profId) {
                $cours_data[$i]["profs"][$k] = $prof->getOne($profId);
            }
            foreach ($cours_data[$i]["raw_classes"] as $k => $classeid) {
                $cours_data[$i]["classes"][$k] = $classe->getOne($classeid);
            }
        }
        
        return $cours_data;
    }
}
