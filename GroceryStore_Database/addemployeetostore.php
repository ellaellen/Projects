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
  
    $firstname = $_POST['efname'];
    $lastname = $_POST['elname'];
    $job = $_POST['job'];
    $query = "INSERT INTO gw_employee_salary(emp_id,jobtitle) SELECT emp_id,? FROM gw_employees  WHERE first_name = '$firstname' AND last_name = '$lastname' ";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param('s', $job))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to employee salary table.";
    }
 
?>

<div>
<p>The existing employees in all the stores are:</p>
<table>
<tr>
<td>Employee ID</td>
<td>Store ID</td>
<td>First Name</td>
<td>Last Name</td>
<td>Job Title</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT gw_employees.emp_id, gw_employees.store_id, gw_employees.first_name, gw_employees.last_name,gw_employee_salary.jobtitle FROM gw_employees INNER JOIN gw_employee_salary ON gw_employees.emp_id = gw_employee_salary.emp_id"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($eid, $sid, $efname, $elname,$job)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $eid. "\n</td>\n<td>\n" . $sid . "\n</td>\n<td>\n".$efname . "\n</td>\n<td>\n" . $elname . "\n</td>\n<td>\n". $job. "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>



</body>



</html>

