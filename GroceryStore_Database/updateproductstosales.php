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
  
    $sale = (int)$_POST['sale'];
    $name = $_POST['Name'];
    $quantity = (int)$_POST['quantity'];
    $query = "UPDATE  gw_sales_details SET  quantity =  ? WHERE  gw_sales_details.sid = $sale AND  gw_sales_details.item_id IN (SELECT gw_products.product_id FROM gw_products WHERE gw_products.name = '$name')  LIMIT 1 ";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param('i', $quantity))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Updated " . $stmt->affected_rows . " rows to sales table.";
    }
 
?>

<div>
<p>The existing products in the selected sale are:</p>
<table>
    <tr>
        <td>Product Name</td>
        <td>Quantity</td>
    </tr>
<?php
    $sale = $_POST['sale']; 
    $query = "SELECT gw_products.name, gw_sales_details.quantity FROM gw_products INNER JOIN gw_sales_details ON gw_sales_details.item_id = gw_products.product_id WHERE gw_sales_details.sid = '$sale'";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param("s",$_POST['Name']))){
     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
     }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->bind_result($name, $quantity)) {
        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    while ($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $name . "\n</td>\n<td>\n" . $quantity . "\n</td>\n</tr>";
    }
    
    $stmt->close();
    
    
    ?>
</table>
</div>



</body>



</html>

