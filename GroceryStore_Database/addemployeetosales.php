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
    $efname = $_POST['fname'];
    $elname = $_POST['lname'];
    $cfname = $_POST['cfname'];
    $clname = $_POST['clname'];
    $sale = $_POST['sale']; 
    $query = "INSERT INTO gw_sales_withemp(sale_id, employee_id, customer_id) SELECT $sale, gw_employees.emp_id,gw_customer.customer_id FROM gw_employees, gw_customer WHERE gw_employees.first_name = '$efname' AND gw_employees.last_name = '$elname' AND gw_customer.first_name = '$cfname' AND gw_customer.last_name = '$clname'";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param('i',$quantity))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to employee customer sales table.";
    }
 
?>

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
    $sale = $_POST['sale']; 
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

