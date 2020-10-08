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
    $joindate = $_POST['Joindate'];
    $query = "INSERT INTO gw_customer_membership( cid, sid, join_date) SELECT customer_id, sid,? FROM gw_customer,gw_stores  WHERE gw_stores.city = '$store' AND gw_customer.first_name = '$firstname' AND gw_customer.last_name = '$lastname'";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param('s',$joindate))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to customer store membership table.";
    }
 
?>

<div>
<p>The existing customers in the selected store are:</p>
<table>
    <tr>
        <td>First Name</td>
        <td>Last Name</td>
    </tr>
<?php
    $store = $_POST['store']; 
    $query = "SELECT gw_customer.first_name, gw_customer.last_name FROM gw_customer INNER JOIN gw_customer_membership ON gw_customer_membership.cid = gw_customer.customer_id INNER JOIN gw_stores ON gw_stores.sid = gw_customer_membership.sid WHERE gw_stores.city = '$store'";
    
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

