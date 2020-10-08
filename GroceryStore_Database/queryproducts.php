<!DOCTYPE html >

<html>

<body>
<font color = "blue", size = '5'>
        Search Products
</font>
<br><br>

<p>
Please fill in the following infomation to search products in the database
</p>

<div>
    <form action="searchproducts.php" method="post" >
        <fieldset>
            <legend>Filter by</legend>
            <p>SupplyCompany
            <select name = "supplier">
                <option> </option>
                <option>NESTLE</option><option>HEINZ</option>
                <option>TROPICANA</option><option>GOOD HAVEN</option>
                <option>KRAFT</option><option>LUCERNE</option>
                <option>WHOLESOME FOOD</option><option>LOCAL</option>
                <option>FARMANDYOU</option>
            </select>
            <a href="supplycompany.html">Add Supplier here</a>
            </p>
        
            <p>Expire Before the Date(YYYY-MM-DD)<input type = "text" name = "ExpireDate"/></p>
        
        </fieldset>
        
        <p><input type = "submit" name = "SearchProducts" value = "Retrieve"/></p>
    </form>
</div>

<div>
<p>The existing products are:</p>
<table>
<?php
    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    $query = "SELECT name FROM gw_products";
    
    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    /*if(!($stmt->bind_param("s",$_POST['Name']))){
     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
     }*/
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->bind_result($name)) {
        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
    }
    
    while ($stmt->fetch()){
        echo  "<tr>\n<td>\n" . $name . "\n</td>\n</tr>";
    }
    
    $stmt->close();
    
    
    ?>
</table>
</div>











</body>



</html>
