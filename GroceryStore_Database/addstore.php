<!DOCTYPE html>
<html>

<body>
<?php

    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
	}
    $city = $_POST['CityName'];
    $fname = $_POST['fName'];
    $lname = $_POST['lName'];
    $query = "INSERT INTO gw_stores(manager_id, city) 
        SELECT gw_employees.emp_id, $city
        FROM gw_employees
        WHERE gw_employees.first_name= $fname AND gw_employees.last_name = $lname"

    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param("sss", $city, $fname, $lname))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to store table.";
    }



?>

</body>
</html>
