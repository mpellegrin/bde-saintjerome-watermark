<?php
require_once('auth.php');

header('Content-Type: application/json');

define('VOTE_PLUS', 1);
define('VOTE_MINUS', 2);
define('VOTE_NULL', 0);

if (!$_COOKIE['uuid'] || !preg_match('/^[a-z0-9]{40}$/', $_COOKIE['uuid'])) {
	$uuid = sha1(uniqid(rand(), true));
	setcookie('uuid', $uuid, time() + 86400*365); // 86400 = 1 day
} else {
	$uuid = $_COOKIE['uuid'];
}

$votes_dir = 'cache/votes/' . $album;
if (!file_exists($votes_dir)) {
	mkdir($votes_dir);
} elseif (!is_dir($votes_dir)) {
	die('Unexpected error.');
} else {
	$vote = $_GET['vote'];
	if ($vote > 0) {
		$vote = VOTE_PLUS;
	} elseif ($vote < 0) {
		$vote = VOTE_MINUS;
	} else {
		$vote = VOTE_NULL;
		die();
	}

	$vote_file = $votes_dir . '/' . $photo;
	if (!is_file($vote_file)) {
		$handle = fopen($vote_file, 'a');
		fwrite($handle, $uuid . ' ' . $vote);
		fclose($handle);
	} else {
		$votes = file_get_contents($vote_file);
		if (($pos = strpos($votes, $uuid)) !== false) {
			$votes = substr_replace($votes, $vote, $pos+strlen($uuid)+1); // Possible overflow
			$handle = fopen($vote_file, 'w');
			fwrite($handle, $votes);
			fclose($handle);
		} else {
			$handle = fopen($vote_file, 'a');
			fwrite($handle, "\n" . $uuid . ' ' . $vote);
			fclose($handle);
		}
	}

	$votes = file($vote_file);
	$score = 0;
	foreach ($votes as $vote) {
		$vote = explode(' ', $vote);
		if ($vote[1] == VOTE_PLUS)
			$score++;
		elseif ($vote[1] == VOTE_MINUS)
			$score--;
	}
	echo json_encode($score);
}

