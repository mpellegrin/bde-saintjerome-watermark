<?php

session_start();

if (!isset($_SESSION['album']) || empty($_SESSION['album'])) {
	die('Session error');
}

header('Content-Type: application/json');

// A list of permitted file extensions
$allowed = array('png', 'jpg', 'gif');

if(isset($_FILES['upl']) && $_FILES['upl']['error'] == 0){

	$extension = pathinfo($_FILES['upl']['name'], PATHINFO_EXTENSION);

	$cwd = realpath(__DIR__);
	$upload_dir = realpath($cwd . '/../photos/');
	$album_dir = $upload_dir . '/' . $_SESSION['album'];

	if(!in_array(strtolower($extension), $allowed) || empty($_SESSION['album']) || !file_exists($album_dir) || !is_dir($album_dir)){
		echo '{"status":"error"}';
		exit;
	}

	if(move_uploaded_file($_FILES['upl']['tmp_name'], $album_dir.'/'.$_FILES['upl']['name'])){
		echo '{"status":"success"}';
		exit;
	}
}

echo '{"status":"error"}';
exit;
