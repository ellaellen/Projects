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
 Add/Update/Delete EMPLOYEES to EMPLOYEE-STORE RELATIONSHIP 
</font>
 
<br><br>

<p>
Please fill in the following info to add or update supplier for the products to the database.
</p>

<div>
    <form method="post" action = "addsuppliertoproducts.php">


<fieldset>
<legend>Product Name</legend>
<p>Name:
<select name = "pname"/>
<option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT name FROM gw_products ORDER BY name"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($name)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $name . '</option>\n';
    }
    $stmt->close();
    ?>
</select>
</p>
</fieldset>



        <fieldset>
            <legend>Supplier</legend>
            <p>Name:
<select name = "sname"/>
<option></option>
<?php
    if(!($stmt = $mysqli->prepare("SELECT name FROM gw_products_supplier ORDER BY name"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($name)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo '<option> ' . $name . '</option>\n';
    }
    $stmt->close();
    ?>


</select>
</p>
        </fieldset>
        

        <p><input type = "submit" name = "Add" value = "add supplier"/></p>
        <p><input type = "submit" name = "Update" value = "update supplier"/></p>
    </form>
</div>

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

<div>
<p>The existing products in all the stores are:</p>
<table>
<tr>
<td>Product ID</td>
<td>Product Name</td>
</tr>

<?php
    
    if(!($stmt = $mysqli->prepare("SELECT product_id, name FROM gw_products"))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    
    if(!$stmt->execute()){
        echo "Execute failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    if(!$stmt->bind_result($id, $name)){
        echo "Bind failed: "  . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    while($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $id. "\n</td>\n<td>\n" . $name ."\n</td>\n\n</tr>";
    }
    $stmt->close();
    ?>

</table>
</div>



</body>



</html>
