<?php
/* 
* 
* This script send email when user fills in the form
* Check out this tutorial on PHP forms http://myphpform.com/php-form-tutorial.php or this http://www.tizag.com/phpT/forms.php one
*
*/

$to = "acrolama@acrolama.com";
$subject = "Signup from Ventcamp";
$message = "Ticket type: " . $_POST['option'];
$message .= "<br/>Fullname: " . $_POST['name'];

$headers  = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type: text/html; charset=utf-8" . "\r\n";
$headers .= "From: " . $_POST['name'] . " <" . $_POST['email'] . ">". "\r\n";

if( mail($to, $subject, $message, $headers) ) {
	echo "ok";
} else {
	echo "error";
}