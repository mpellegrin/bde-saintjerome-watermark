<?php

session_start();

if (isset($_SESSION['album']) && $_SESSION['album'] == $_GET['album']) {
	$result = true;
} else {

	$album_name = $_GET['album'];

	$album_name = str_replace('/', '-', $album_name);
	$album_name = str_replace('.', '', $album_name);
	$album_name = trim($album_name);

	$cwd = realpath(__DIR__);
	$upload_dir = realpath($cwd . '/../photos/');
	$album_dir = $upload_dir . '/' . $album_name;

	$_SESSION['album'] = $album_name;

	if (!file_exists($album_dir) && !empty($_GET['album']))
		$result = mkdir($album_dir);
	else
		$result = false;
}

if (!$result) {
	unset($_SESSION['album']);
}

header('Content-Type: application/json');
echo json_encode($result);


