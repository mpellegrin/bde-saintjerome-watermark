<?php

// Just keep session alive...

session_start();

if (!isset($_SESSION['album']) || empty($_SESSION['album'])) {
	die('Session error');
}

