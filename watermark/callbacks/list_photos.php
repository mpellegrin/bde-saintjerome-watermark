<?php

session_start();

if (!isset($_SESSION['album']) || empty($_SESSION['album'])) {
	die('Session error');
}

$cwd = realpath(__DIR__);
$upload_dir = realpath($cwd . '/../photos/');
$album_dir = realpath($upload_dir . '/' . $_SESSION['album']);

$files_list = null;
if ($album_dir && !empty($_SESSION['album'])) {
	$files_list = scandir($album_dir);

	// "." and ".."
	array_shift($files_list);
	array_shift($files_list);
}

header('Content-Type: application/json');
echo json_encode($files_list);

