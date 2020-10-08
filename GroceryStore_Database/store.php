<!DOCTYPE html >

<html>

<body>
    
 <font color = "blue", size = '5'>
 Add, Update and Delete STORES
</font>
 
<br><br>

<p>

Please fill in the following infomation to add, delete or update stores to the database

</p>
<div>
    <form action="addstore.php" method="post" >
        <fieldset>
            <legend>Store Location</legend>
            <p>City: <input type = "text" name = "CityName"/></p>
        </fieldset>
        <fieldset>
            <legend> Manager</legend>
            <p>First Name<input type = "text" name = "fName"/></p>
            <p>Last Name<input type = "text" name = "lName"/></p>
            <a href="employee.php">Add New Employee here</a>
        </fieldset>
        <p><input type = "submit" name = "Add" value = "Add Store"/></p>
    </form>
</div>


<div>
<p>The existing stores are:</p>
<table>
<tr>
<td>Store ID</td>
<td>Manager Employee ID</td>
<td>City</td>
</tr>

<?php
                    //Turn on error reporting
                    ini_set('display_errors', 'On');
                    //Connects to the database
                    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
                    if(!$mysqli || $mysqli->connect_errno){
                        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                    }

                    $query = "SELECT sid, manager_id, city FROM gw_stores";

                    if(!($stmt = $mysqli->prepare($query))){
                        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
                    }
                    /*if(!($stmt->bind_param("s",$_POST['Name']))){
                     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
                    }*/
                    if(!$stmt->execute()){
                        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
                    }
                    if(!$stmt->bind_result($sid, $mid, $city)) {
                        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                    }

                    while ($stmt->fetch()){
                        echo  "<tr>\n<td>\n" . $sid . "\n</td>\n<td>\n". $mid. "\n</td>\n<td>\n". $city. "\n</td>\n</tr>";
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
<td>First Name</td>
<td>Last Name</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT emp_id, first_name, last_name FROM gw_employees"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($eid, $efname, $elname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $eid. "\n</td>\n<td>\n" . $efname . "\n</td>\n<td>\n" . $elname . "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>








</body>



</html>
