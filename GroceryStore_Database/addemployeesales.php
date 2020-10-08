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
 Add EMPLOYEES/Customers to SALES
</font>
 
<br><br>

<p>
Please fill in the following info to add,update or delete sales in the database.
</p>

<div>
    <form  id = "employeesales" method="post" action = "addemployeetosales.php">
<fieldset>
<legend>Sale ID</legend>
<p>Sale ID<input type = "text" name = "sale"/></p>
</fieldset>

        <fieldset>
            <legend>Employee</legend>
            <p>First Name:
            <select name = "fname">
            <option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT first_name FROM gw_employees"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }   
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($fname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $fname . '</option>\n';
    }
    $stmt->close();
?>
            </select>
            </p>
            <p>Last Name:
            <select name = "lname">
            <option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT last_name FROM gw_employees"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }   
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($lname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $lname . '</option>\n';
    }
    $stmt->close();
?>
            </select>
            </p>

        </fieldset>
        
        <fieldset>
            <legend>Customer Name</legend>
            <p>First Name:
            <select name = "cfname"/>
            <option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT first_name FROM gw_customer"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result( $cfname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $cfname . '</option>\n';
    }
    $stmt->close();
?>

            </select>
            </p>
            <p>Last Name: 
            <select name = "clname"/>
            <option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT last_name FROM gw_customer"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result( $clname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $clname . '</option>\n';
    }
    $stmt->close();
?>

            </select>
            </p>
        </fieldset>


<script>
function submitForm(action)
{
    document.getElementById('employeesales').action = action;
    document.getElementById('employeesales').submit();
}
</script>

        <p><input type="button" onclick="submitForm('addemployeetosales.php')" value = "add"/></p>
    </form>
</div>

<div>
<p>The existing employees  are:</p>
<table>
<tr>
<td>First Name</td>
<td>Last Name</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT first_name, last_name FROM gw_employees"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($efname, $elname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $efname . "\n</td>\n<td>\n" . $elname . "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>

<div>
<p>The existing Customers are:</p>
<table>
<tr>
<td>First Name</td>
<td>Last Name</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT first_name, last_name FROM gw_customer"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($cfname, $clname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $cfname . "\n</td>\n<td>\n" . $clname . "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>

<div>
<p>The existing sales are:</p>
<table>
<tr>
<td>Sale ID</td>
<td>Employee</td>
<td></td>
<td>Customer</td>
</tr>
<?php
    $query = "SELECT gw_sales_withemp.sale_id, gw_employees.first_name, gw_employees.last_name, gw_customer.first_name, gw_customer.last_name FROM gw_sales_withemp INNER JOIN gw_employees ON gw_sales_withemp.employee_id = gw_employees.emp_id INNER JOIN gw_customer ON gw_customer.customer_id = gw_sales_withemp.customer_id";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param())){
     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
     }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->bind_result($id, $efname, $elname, $cfname, $clname)) {
        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    while ($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $id . "\n</td>\n<td>\n" . $efname . "\n</td>\n<td>\n". $elname. "\n</td>\n<td>\n". $cfname. "\n</td>\n<td>\n". $clname. "\n</td>\n</tr>";
    }
    
    $stmt->close();
    
    
    ?>
</table>
</div>






</body>



</html>
