<?php
require_once('config.php');

$base_uri = $config['base_uri'];
$request_uri = rawurldecode($_SERVER['REQUEST_URI']);

$thumb = substr($request_uri, strlen($base_uri));

$path = explode('/', $thumb);
if (count($path) != 4 || $path[0] != 'cache') {
	exit();
}

$format = $path[1];
if ($format != 'thumbs' && $format != 'mediums') {
	exit();
}

$album = $path[2];
if ($album == '.' ||  $album =='..') {
	exit();
}

$filename = $path[3];
if ($filename == '.' ||  $filename =='..') {
	exit();
}


$thumb_dir = 'cache/' . $format . '/' . $album;
if (file_exists($thumb_dir) && !is_dir($thumb_dir)) {
	exit();
}
if (!file_exists($thumb_dir)) {
	mkdir($thumb_dir);
}
$src = 'originals/' . $path[2] . '/' . $filename;

if (!file_exists($thumb)) {
	/* read the source image */
	$source_image = imagecreatefromjpeg($src);
	$width = imagesx($source_image);
	$height = imagesy($source_image);
	
	switch ($format) {
		case 'mediums':
			$thumb_width = 800;
			/* find the "desired height" of this thumbnail, relative to the desired width  */
			$thumb_height = floor($height * ($thumb_width / $width));

			/* create a new, "virtual" image */
			$virtual_image = imagecreatetruecolor($thumb_width, $thumb_height);
			
			/* copy source image at a resized size */
			imagecopyresampled($virtual_image, $source_image, 0, 0, 0, 0, $thumb_width, $thumb_height, $width, $height);
		break;

		case 'thumbs': 
			$thumb_width = 100;
			$thumb_height = 100;

			$original_aspect = $width / $height;
			$thumb_aspect = $thumb_width / $thumb_height;

			if ( $original_aspect >= $thumb_aspect )
			{
			   // If image is wider than thumbnail (in aspect ratio sense)
			   $new_height = $thumb_height;
			   $new_width = $width / ($height / $thumb_height);
			}
			else
			{
			   // If the thumbnail is wider than the image
			   $new_width = $thumb_width;
			   $new_height = $height / ($width / $thumb_width);
			}

			/* create a new, "virtual" image */
			$virtual_image = imagecreatetruecolor($thumb_width, $thumb_height);
			
			/* copy source image at a resized size */
			imagecopyresampled($virtual_image, $source_image, (0-($new_width-$thumb_width)/2), (0-($new_height-$thumb_height)/2), 0, 0, $new_width, $new_height, $width, $height);
		break;

		default:
			exit();
		break;
	}
	
	/* create the physical thumbnail image to its destination */
	imagejpeg($virtual_image, $thumb);
}

if (file_exists($thumb) && is_file($thumb)) {
	header('Content-type: image/jpeg');
	echo file_get_contents($thumb);
}
