<?php

session_start();

if (!isset($_SESSION['album']) || empty($_SESSION['album'])) {
	die('Session error');
}

$cwd = realpath(__DIR__);
chdir($cwd);
$watermarked_dir = realpath($cwd . '/../watermarked/');
$album_dir = $watermarked_dir . '/' . $_SESSION['album'];

if (!file_exists($album_dir) && !empty($_SESSION['album']))
	mkdir($album_dir);

setlocale(LC_ALL, 'fr_FR.UTF-8');
$result = shell_exec(__DIR__ . '/watermark.py ' . escapeshellarg($_SESSION['album']) . ' ' . escapeshellarg($_GET['file_name']) . ' ' . escapeshellarg($_GET['text']));

header('Content-Type: application/json; charset=UTF-8');
echo json_encode($result);


