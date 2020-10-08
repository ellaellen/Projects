<!DOCTYPE html>
<html>
<head>
    <title> Search Customers results</title>
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
	
    
    $query = "SELECT cus.first_name, cus.last_name FROM gw_customer cus INNER JOIN gw_customer_membership cusmem ON cusmem.cid = cus.customer_id INNER JOIN gw_stores stores ON stores.sid = cusmem.sid WHERE stores.city = [store] AND cusmem.join_date > [JoinDate]";

    if(!($stmt = $mysqli->prepare($query))){
        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!($stmt->bind_param("s",$first_name, $last_name))){
        echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
    }
    if(!$stmt->execute()){
        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
    }
    while ($stmt->fetch()){
        echo "<tr>\n<td>\n". $first_name . "\n</td>\n<td>\n" . $last_name. "\n</td>\n</tr>";
    }
    
    $stmt->close();


?>

</body>
</html>
