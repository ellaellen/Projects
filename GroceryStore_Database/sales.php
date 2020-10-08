<?php
                //Turn on error reporting
                ini_set('display_errors', 'On');
                //Connects to the database
                $mysqli = new mysqli("oniddb.cws.oregonstate.edu","wujiao-db","cUhlYd6WZm2g9lqP","wujiao-db");
                if (!$mysqli || $mysqli->connect_errno) {
                    echo "Connection error " . $mysqli->connect_errno . " " . $mysqli->connect_error;
                }

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>

<body>
    
<font color = "blue", size = '5'>
 Add and Update SALES
</font>
 
<br><br>

<p>

Please fill in the following infomation to add or update sales to the database

</p>
<div>
    <form action="addsales.php" method="post" >
        <fieldset>
            <legend>Employee ID</legend>
            <p>Employee ID:
            <select name = "employeeid">

            </select>
            </p>
        </fieldset>

        <fieldset>
            <legend>Customer ID</legend>
            <p>Customer ID
            <select name = "customerid">





            </select>

            </p>
        </fieldset>

        <fieldset>
            <legend>Store</legend>
            <p>Store 
            <select name = "storeid">




            </select>

            </p>
        </fieldset>

        <fieldset>
            <legend>SALE Date</legend>
            <p>Year:
            <select name = "saleyear"/>
                <?php
                for ($i=2000; $i<=2014; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>

            <p>Month:
            <select name = "salemonth"/>
                <?php
                for ($i=1; $i<=12; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>

            <p>Day:
            <select name = "saledate"/>
                <?php
                for ($i=1; $i<=31; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>

            <p>Hour:
            <select name = "salehour"/>
                <?php
                for ($i=8; $i<=23; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>

            <p>Min:
            <select name = "salemin"/>
                <?php
                for ($i=0; $i<=59; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>

            <p>Second:
            <select name = "salesec"/>
                <?php
                for ($i=0; $i<=59; $i++)
                {
                ?>
                <option value="<?php echo $i;?>"><?php echo $i;?></option>
                <?php
                }
                ?>            
            </select>
            </p>
        </fieldset>

        <fieldset>
            <legend>Pay Method</legend>
            <p>Pay by
            <select name = "paymethod">
                <option></option>
                <option>VISA</option>
                <option>MASTERCARD</option>
                <option>CASH</option>
                <option>CHEQUE</option>
                </p>
            </fieldset>

        <fieldset>
            <legend>SUBTOTAL</legend>
            <p>SUBTOTAL:<input type = "text" name = "subtotal"/></p>
        </fieldset>

            <p><input type = "submit" name = "Add" value = "Add Sales"/></p>
            <p><input type = "submit" name = "Update" value = "Update Sales"/></p>
        </form>
    </div>

</body>



</html>
