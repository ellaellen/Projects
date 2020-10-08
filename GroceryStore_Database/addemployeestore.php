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
    
 <font color = "blue", size = '5'>
 Add/Update/Delete EMPLOYEES to EMPLOYEE-STORE RELATIONSHIP 
</font>
 
<br><br>

<p>
Please fill in the following info to add or update employee to the database.
</p>

<div>
    <form method="post" action = "addemployeetostore.php">
        
        <fieldset>
            <legend>Existing Employee Name</legend>
            <p>First Name: <input type = "text" name = "efname"/></p>
            <p>Last Name: <input type = "text" name = "elname"/></p>
            <a href = "employee.php">Add New Employee Here</a>
        </fieldset>

        <fieldset>
            <legend>Job Title</legend>
            <p>Job Title <input type = "text" name = "job"/></p>
        </fieldset>
        

        <p><input type = "submit" name = "Add" value = "add employee"/></p>
        <p><input type = "submit" name = "Update" value = "update employee"/></p>
    </form>
</div>

<div>
<p>The existing employees with job titles are:</p>
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

<div>
<p>The existing employees in all the stores are:</p>
<table>
<tr>
<td>Employee ID</td>
<td>Store ID</td>
<td>First Name</td>
<td>Last Name</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT emp_id, store_id, first_name, last_name FROM gw_employees"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($eid, $sid, $efname, $elname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $eid. "\n</td>\n<td>\n" . $sid . "\n</td>\n<td>\n".$efname . "\n</td>\n<td>\n" . $elname . "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>



</body>



</html>
