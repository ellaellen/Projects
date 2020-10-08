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
<head>
    <title> Search Products results</title>
</head>

<body>
<div>
    <table>
        <tr>
            <td>Products</td>
        </tr>
        <tr>
            <td>Name</td>
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
    $supplier = $_POST['supplier'];
    $expire = $_POST['ExpireDate'];
    $query = "SELECT gw_products.name FROM gw_products INNER JOIN gw_products_supplier ON gw_products_supplier.supplier_id=gw_products.supply_company WHERE expire_date < '$expire' AND gw_products_supplier.name = '$supplier'";

    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }

    /*if(!($stmt->bind_param("ss",$expire, $supplier))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }*/
    

    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } 
    if(!($stmt->bind_result($name))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }

    while ($stmt->fetch()){
        echo "<tr>\n<td>\n". $name . "\n</td>\n\n</tr>";
    }
      
    $stmt->close();
     
?>
    </table>
</div>

</body>
</html>
