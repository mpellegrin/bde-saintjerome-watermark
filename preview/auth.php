<?php
require_once('config.php');

session_start();

$album = @$_GET['album'];
$photo = @$_GET['photo'];
$vote = @$_GET['vote'];
$token = @$_GET['token'];
$info_message = '';

if (($token && $album) || (@$_SESSION['opened'] && $album)) {
	if (strstr('/', $token) === false && strstr('\\', $token) === false && strstr('/',  $album) === false && strstr('\\', $album) === false)  {
		$filename = 'cache/tokens/' . $album . '/' . $token;
		if (!@$_SESSION['opened'] && (!file_exists($filename) || !is_file($filename))) {
			die('The link you followed is incorrect or outdated');
		} else {
			if (!file_exists('originals/' . $album) || !is_dir('originals/' . $album)) {
				exit();
			}
			$images_list = scandir('originals/' . $album);
			foreach ($images_list as $index => $img) {
				if (!is_file('originals/' . $album . '/' . $img)) {
					unset($images_list[$index]);
				}
			}
			unset($img);
			unset($idx);
			sort($images_list);
		}
	} else {
		exit();
	}
} else {
	if (!$album && !$token) {
		if (@$_SESSION['opened'] != true && $config['password'] && @$_POST['password'] != $config['password']) {
			?>
				<form method="post">
					Mot de passe : <input type="password" name="password" />
					<input type="submit" />
				</form>
			<?php
			exit();
		} else {
			$_SESSION['opened'] = true;
			$albums_list = scandir('originals/');
			foreach ($albums_list as $index => $alb) {
				if (!(is_dir('originals/' . $alb) || (is_link('originals/' . $alb) && is_dir(realpath('originals/' . $alb . '/')))) || $alb == '.' || $alb == '..') {
					unset($albums_list[$index]);
				}
			}
			unset($album);
			unset($index);
			sort($albums_list);
		}
	} else {
		die('The link you followed is incorrect or outdated');
	}
}
