<?php
    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

<body>
<div>
    <table>
        <tr>
            <td>Employees</td>
        </tr>
        <tr>
            <td>First Name</td>
            <td>Last Name</td>
        </tr>
<?php	
    /*
    $query = "SELECT name,unit_price FROM gw_products";
    if ($query_run = mysqli->query($query)){
        echo "query success";
        while ($row = mysqli_fetch_array($query_run)){
            $name = $row['name'];
            $unit_price = $row['unit_price'];
            echo $name.' '.$unit_price;
        }
    }
    else
        echo "query failed.";
     */
    /*
    $result = mysqli_query($mysqli, $query);
    if (!$result){
        echo "Prepare failed: ";
    }

    while ($row = mysqli_fetch_array($result)) {
        echo "<tr>\n<td>\n". $row['name'] . "\n</td>\n<td>\n\n</tr>";
    }
    mysqli_close($mysqli);
     */
    $store = $_POST['store'];
    $job = $_POST['job'];
    $joindate = $_POST['JoinDate'];
    $query = "SELECT gw_employees.first_name, gw_employees.last_name FROM gw_employees INNER JOIN gw_stores ON gw_stores.sid = gw_employees.store_id INNER JOIN gw_employee_salary ON gw_employee_salary.emp_id = gw_employees.emp_id WHERE gw_stores.city =  '$store' AND gw_employee_salary.jobtitle = '$job' AND gw_employees.hire_date > '$joindate' ";

    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }

    /*if(!($stmt->bind_param("sss",$store, $job, $joindate))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }*/
    

    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } 
    if(!($stmt->bind_result($firstname, $lastname))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
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
