<!DOCTYPE html >

<html>

<body>
    
 <font color = "blue", size = '5'>
 Add, Update and Delete CUSTOMERS
</font>
 
<br><br>

<p>

Please fill in the following infomation to add, delete or update customers to the database

</p>
<div>
    <form action="addcustomer.php" method="post" >
        <fieldset>
            <legend> Customer</legend>
            <p>First Name<input type = "text" name = "fName"/></p>
            <p>Last Name<input type = "text" name = "lName"/></p>
            <p>Birthdate(YYYY-MM-DD)<input type = "text" name = "date"/></p>
        </fieldset>
        <p><input type = "submit" name = "Add" value = "Add Customer"/></p>
    </form>
</div>


<div>
<p>The existing customers are:</p>
<table>
<tr>
<td>First Name</td>
<td>Last Name</td>
</tr>

<?php
                    //Turn on error reporting
                    ini_set('display_errors', 'On');
                    //Connects to the database
                    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
                    if(!$mysqli || $mysqli->connect_errno){
                        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                    }

                    $query = "SELECT first_name, last_name FROM gw_customer";

                    if(!($stmt = $mysqli->prepare($query))){
                        echo "Prepare failed: "  . $stmt->errno . " " . $stmt->error;
                    }
                    /*if(!($stmt->bind_param("s",$_POST['Name']))){
                     echo "Bind failed: "  . $stmt->errno . " " . $stmt->error;
                    }*/
                    if(!$stmt->execute()){
                        echo "Execute failed: "  . $stmt->errno . " " . $stmt->error;
                    }
                    if(!$stmt->bind_result($fname, $lname)) {
                        echo "Bind failed: " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                    }

                    while ($stmt->fetch()){
                        echo  "<tr>\n<td>\n" . $fname . "\n</td>\n<td>\n". $lname. "\n</td>\n</tr>";
                    }

                    $stmt->close();


?>
</table>
</div>




</body>



</html>
