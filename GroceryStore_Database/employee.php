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
 Add/Update/Delete EMPLOYEES 
</font>
 
<br><br>

<p>
Please fill in the following info to add or update employee to the database.
</p>

<div>
    <form method="post" action = "addemployee.php">
        <fieldset>
            <legend>Store</legend>
            <p>Store Location:
            <select name = "store">
                <option></option>
                <option>TORONTO</option><option>CALGARY</option>
                <option>NEW YORK</option><option>LOS ANGELES</option>
            </select>
            </p>
        </fieldset>
        
        <fieldset>
            <legend>Name</legend>
            <p>First Name: <input type = "text" name = "FirstName"/></p>
            <p>Last Name: <input type = "text" name = "LastName"/></p>
        </fieldset>

        <fieldset>
            <legend>Birth_date</legend>
            <p>Birthdate(YYYY-MM-DD) <input type = "text" name = "Birthdate"/></p>
        </fieldset>
        
        <fieldset>
            <legend>Hire_date</legend>
            <p>Hiredate(YYYY-MM-DD) <input type = "text" name = "Hiredate"/></p>
        </fieldset>

        <fieldset>
            <legend>Email</legend>
            <p>Email <input type = "text" name = "Email"/></p>
        </fieldset>
        
        <fieldset>
            <legend>PhoneNumber</legend>
            <p>PhoneNumber <input type = "text" name = "PhoneNumber"/></p>
        </fieldset>

        <p><input type = "submit" name = "Add" value = "add employee"/></p>
    </form>
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
