<!DOCTYPE html>
<html>
<head>
    <title> Add Products results</title>
</head>

<body>
<?php

    //Turn on error reporting
    ini_set('display_errors', 'On');
    //Connects to the database
    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
    if(!$mysqli || $mysqli->connect_errno){
        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
	}
	

//  if (!$   || !$   ){
  //    echo 'You have not entered search details. Please go back and try again.';
    //  exit;
  //}

  //if (!get_magic_quotes_gpc()){

  //}

  //perform query
  //$query = "  ";
  //$result = $db->query($query);
    
    $query = "INSERT INTO gw_products(name, department, supply_company, unit_price, quantity_instock, expire_date, buy_price) 
        SELECT [name],dept.dept_id, prod_supp.supplier_id, [unit_price], [quantity_instock], [expire_date],[buy_price]
        FROM gw_departments dept, gw_products_supplier prod_supp
        WHERE dept.name = [department] AND prod_supp.name = [supply_company]"

    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param("sssdisd",$_POST['Name'],$_POST['Department'],$_POST['Supplier'],$_POST['UnitPrice'],$_POST['QuantityInStock'], $_POST['ExpireDate'],$_POST['BuyPrice']))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    } else {
        echo "Added " . $stmt->affected_rows . " rows to products table.";
    }



?>

</body>
</html>
