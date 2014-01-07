<?php
$i = $_GET["nr"];
#$data = array("username" => "Hagrid", "body" => "new tweet15");                                                                    
$data = array("username" => "pissor", "body"=>"blablub$i");
#$data = array("friend"=>"pissor", "username"=>"dumbledore" );
#$data = array("username"=>"dumbledore", "body"=>"blabla dubmledore");                                                                 
$data_string = json_encode($data);                                                                                   

$ch = curl_init('http://127.0.0.1:5000/post_tweet');
                                                                   
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
curl_setopt($ch, CURLOPT_HTTPHEADER, array(                                                                          
    'Content-Type: application/json',                                                                                
    'Content-Length: ' . strlen($data_string))                                                                       
);

$result = curl_exec($ch);

echo $result;
?>
