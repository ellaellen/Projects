<!DOCTYPE html >

<html>

<body>
    
 <font color = "blue", size = '5'>
 Add, Update and Delete DEPARTMENTS
</font>
 
<br><br>

<p>

Please fill in the following infomation to add, delete or update departments to the database

</p>
<div>
    <form action="adddepartments.php" method="post" >
        <fieldset>
            <legend>Department Name</legend>
            <p>Name: <input type = "text" name = "DeptName"/></p>
        </fieldset>
        <p><input type = "submit" name = "Add" value = "Add Department"/></p>
    </form>
</div>
<div>
    <form action="deletedepartments.php" method="post" >
        <fieldset>
            <legend>Department Name</legend>
            <p>Name: <input type = "text" name = "DeptName"/></p>
        </fieldset>
        <p><input type = "submit" name = "Delete" value = "Delete Department"/></p>
    </form>
</div>

<div>
    <form action="updatedepartments.php" method="post" >
        <fieldset>
            <legend>Update Department Name</legend>
            <p>Old Name:<input type = "text" name = "oldname"/></p>
            <p>New Name: <input type = "text" name = "newname"/></p>
        </fieldset>
        
        <p><input type = "submit" name = "Update" value = "Update Department"/></p>
    </form>
</div>

<div>
<p>The existing departments are:</p>
<table>
<?php
                    //Turn on error reporting
                    ini_set('display_errors', 'On');
                    //Connects to the database
                    $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
                    if(!$mysqli || $mysqli->connect_errno){
                        echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                    }

                    $query = "SELECT name FROM gw_departments";

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
