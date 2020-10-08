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
 Add/Update/Delete PRODUCTS to SALES
</font>
 
<br><br>

<p>
Please fill in the following info to add,update or delete sales in the database.
</p>

<div>
    <form id="productsales" method="post" action = "addproductstosales.php">
        <fieldset>
            <legend>Sale </legend>
            <p>Sale ID: 
            <input type = "text" name = "sale"/></p>
        </fieldset>
        
        <fieldset>
            <legend>Product Name</legend>
            <p>Name: 
            <select name = "Name"/>
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
            <legend>Quantity</legend>
            <p>Quantity <input type = "text" name = "quantity"/></p>
        </fieldset>

<script>
function submitForm(action)
{
    document.getElementById('productsales').action = action;
    document.getElementById('productsales').submit();
}
</script>

        <p><input type="button" onclick="submitForm('addproductstosales.php')" value = "add product"/></p>
        <p><input type="button" onclick="submitForm('updateproductstosales.php')"value = "update product"/></p>
        <p><input type="button" onclick="submitForm('deleteproductstosales.php')" value = "delete product"/></p>
    </form>
</div>

<div>
<p>The existing products in all the sales are:</p>
<table>
<tr>
<td>Sale ID</td>
<td>Product Name</td>
<td>Quantity</td>
</tr>
<?php
    $query = "SELECT gw_sales_details.sid, gw_products.name, gw_sales_details.quantity FROM gw_products INNER JOIN gw_sales_details ON gw_sales_details.item_id = gw_products.product_id ";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param("s",$_POST['Name']))){
     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
     }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->bind_result($id, $name, $quantity)) {
        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    while ($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $id . "\n</td>\n<td>\n" . $name . "\n</td>\n<td>\n".  $quantity . "\n</td>\n</tr>";
    }
    
    $stmt->close();
    
    
    ?>
</table>
</div>










</body>



</html>
