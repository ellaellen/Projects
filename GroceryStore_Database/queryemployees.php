<!DOCTYPE html >

<html>


<body>
    <font color = "blue", size = '5'>
        Search Employees
    </font>
<br><br>

<p>
Please fill in the following infomation to search employees in the database
</p>

<div>
    <form action="searchemployees.php" method="post" >
        <fieldset>
            <legend>Filter by</legend>
            <p>Store Branch
            <select name = "store">
                <option>ANY</option>
                <option>TORONTO</option><option>CALGARY</option>
                <option>NEW YORK</option><option>LOS ANGELES</option>
            </select>
            </p>
        
            <p>Job Title
            <select name = "job">
                <option>ANY</option>
                <option>SALE REP</option><option>SHIFT SUPERVISOR</option>
                <option>ASSOCIATE MANAGER</option><option>MANAGER</option>
            </select>
            </p>

            <p>Join after the Date(YYYY-MM-DD)<input type = "text" name = "JoinDate"/></p>
        
        </fieldset>
        
        <p><input type = "submit" name = "SearchEmployees" value = "Retrieve"/></p>
    </form>
</div>

<div>
<p>The existing employees are:</p>
<table>
<tr>
<td>First Name</td>
<td>Last Name</td>
</tr>
<?php
    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    $query = "SELECT first_name, last_name FROM gw_employees";
    
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
