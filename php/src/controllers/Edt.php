<?php
require_once ROOT."models/Cours.php";
require_once ROOT."models/Prof.php";
require_once ROOT."models/Classe.php";
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
    public function classe()
    {
        if (array_key_exists("c", $_GET)) {
            $this->render("edt", ["cours"=>$this->getCoursForClasse(explode(",", $_GET["c"]))]);
        } else {
            header('Location: /edt');
            die();
        }   
    }
    public function raw()
    {
        $this->render("raw", ["cours"=>$this->getCleanCours()]);
    }
    private function getCleanCours()
    {
        $cours = new Cours();
        $prof = new Prof();
        $classe = new Classe();
        $cours_data = [];
        foreach ($cours->getAllInTimeOrder() as $i => $data) {
            $cours_data[$i] = ["id"=>$data[0],"nom"=>$data[1],"timestampStart"=>$data[2],"timestampEnd"=>$data[3],"place"=>$data[4],"color"=>$data[5]];

            $cours_data[$i]["raw_profs"] = $cours->getProfIdOfCours($data[0]);
            $cours_data[$i]["raw_classes"] = $cours->getClasseIdOfCours($data[0]);
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

    private function getCoursForClasse(array $classesToFind)
    {
        $coursForClasse = [];
        foreach ($this->getCleanCours() as $cours) {
            $classeDiscovered = false;
            foreach ($cours["classes"] as $classe) {
                if (in_array($classe[0][1], $classesToFind)) {
                    $classeDiscovered = true;
                }   
            }
            if ($classeDiscovered) {
                array_push($coursForClasse, $cours);
            }
        }
        return $coursForClasse;
    }
}
