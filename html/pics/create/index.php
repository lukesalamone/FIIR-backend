<?php
    
echo print_r($_FILES,true);

echo print_r($_POST,true);


    $servername = "localhost";
    $username = "root";
    $password = "1234qwerZ";
    $dbname = "fiir";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } 




?>
