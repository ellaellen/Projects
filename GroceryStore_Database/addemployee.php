<?php
    
    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
	}
?>

<!DOCTYPE html >

<html>

<body>


<?php
  
    $store = $_POST['store'];
    $firstname = $_POST['FirstName'];
    $lastname = $_POST['LastName'];
    $birthdate = $_POST['Birthdate'];  
    $hiredate = $_POST['Hiredate'];
    $email = $_POST['Email'];
    $phonenumber = $_POST['PhoneNumber'];
    $query = "INSERT INTO gw_employees(store_id, first_name, last_name, birth_date, hire_date, email, phonenumber) SELECT sid,?, ?, ?, ?, ?, ? FROM gw_stores  WHERE city = '$store' ";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param('ssssss',$firstname, $lastname, $birthdate, $hiredate, $email, $phonenumber))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to employee table.";
    }
 
?>

<div>
<p>The existing employees in the selected store are:</p>
<table>
    <tr>
        <td>First Name</td>
        <td>Last Name</td>
    </tr>
<?php
    $store = $_POST['store']; 
    $query = "SELECT gw_employees.first_name, gw_employees.last_name FROM gw_employees INNER JOIN gw_stores ON gw_stores.sid = gw_employees.store_id WHERE gw_stores.city = '$store'";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param("s",$_POST['Name']))){
     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
     }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->bind_result($firstname, $lastname)) {
        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    while ($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $firstname . "\n</td>\n<td>\n" . $lastname . "\n</td>\n</tr>";
    }
    
    $stmt->close();
    
    
    ?>
</table>
</div>



</body>



</html>

