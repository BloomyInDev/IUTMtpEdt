<link rel="stylesheet" href="/public/styles/edt.css">
<?php
for ($i=0; $i < count($cours); $i++) { 
    $date = date("d/m/o", $cours[$i]["timestampStart"]);
    $timeStart = date("H:i", $cours[$i]["timestampStart"]);
    $timeEnd = date("H:i", $cours[$i]["timestampEnd"]);
    echo "<div class=\"cours\"><p>";
    echo $cours[$i]["nom"];
    echo "</p><p>$date - $timeStart - $timeEnd</p><p class=\"\">";
    foreach ($cours[$i]["profs"] as $k => $prof) {
        echo $prof[0][1]." ".$prof[0][2];
        if ($k != end(array_keys($cours[$i]["profs"]))) {
            echo " - ";
        }
    }
    echo "</p><p>";
    foreach ($cours[$i]["classes"] as $k => $classe) {
        echo $classe[0][1];
        if ($k != end(array_keys($cours[$i]["classes"]))) {
            echo " - ";
        }
    }
    echo "</p></div>";
}
?>