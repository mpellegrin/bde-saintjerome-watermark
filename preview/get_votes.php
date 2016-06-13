<?php
require_once('auth.php');

define('VOTE_PLUS', 1);
define('VOTE_MINUS', 2);
define('VOTE_NULL', 0);

if ($album && $images_list) {
	$votes_dir = 'cache/votes/' . $album;
	if (file_exists($votes_dir) && is_dir($votes_dir)) {
		$score = array();
		foreach ($images_list as $photo) {
			$vote_file = $votes_dir . '/' . $photo;
			if (file_exists($vote_file) && is_file($vote_file)) {
				$votes = file($vote_file);
				$score[$photo] = 0;
				foreach ($votes as $vote) {
					$vote = explode(' ', $vote);
					if ($vote[1] == VOTE_PLUS)
						$score[$photo]++;
					elseif ($vote[1] == VOTE_MINUS)
						$score[$photo]--;
				}
			}
		}
	}
}
