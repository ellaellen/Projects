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
  
    $pname = $_POST['pname'];
    $sname = $_POST['sname'];
    $query = "INSERT INTO gw_products_withsupply(product_id, supply_company) SELECT gw_products.product_id,gw_products_supplier.supplier_id FROM gw_products, gw_products_supplier WHERE gw_products.name = '$pname' AND gw_products_supplier.name = '$sname' ";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param('i',$quantity))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to products supplier table.";
    }
 
?>


<div>
<p>The existing products with suppliers are:</p>
<table>
<tr>
<td>Product ID</td>
<td>Product Name</td>
<td>Supplier Name</td>
</tr>

<?php
    if(!($stmt = $mysqli->prepare("SELECT gw_products.product_id, gw_products.name, gw_products_supplier.name FROM gw_products INNER JOIN gw_products_withsupply ON gw_products_withsupply.product_id = gw_products.product_id INNER JOIN gw_products_supplier ON gw_products_supplier.supplier_id = gw_products_withsupply.supply_company"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($id, $pname, $sname)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $id. "\n</td>\n<td>\n". $pname. "\n</td>\n<td>\n" . $sname . "\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>



</body>



</html>

