<!DOCTYPE html>
<html>
<head>
    <title> Add Products results</title>
</head>

<body>
<?php

    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
	}
	
    $name = $_POST['DeptName']; 
    $query = "DELETE FROM gw_departments WHERE gw_departments.name = '$name'";  

    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param("s",$_POST['Name']))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Deleted " . $stmt->affected_rows . " rows to departments table.";
    }
    
    $stmt->close();


?>

</body>
</html>
