var callbacks = {};

callbacks['step1'] = function() {
	var album_name = $('input[name=step1]').siblings('input[type=text]').val();
	var result = {status: false, message: 'Erreur inconnue'};
	jQuery.ajax({url: 'callbacks/make_album.php', datatype: 'json', async: false, data: {'album': album_name}, success: function(json) {
		json = jQuery.parseJSON(json);
		if (json == true) {
			result.status = true;
			result.message = '';
		} else {
			result.status = false;
			result.message = 'Impossible de créer le dossier de l\'album.<br />Recommencez en retirant les caractères accentués et spéciaux.'
		}
	} });
	return result;
};

callbacks['step3'] = function() {
	var album_name = $('input[name=step1]').siblings('input[type=text]').val();
	var watermark_text = $('input[name=step3]').siblings('input[type=text]').val();
	var result = {status: false, message: 'Erreur inconnue'};
	var files_list = null;
	jQuery.ajax({url: 'callbacks/list_photos.php', datatype: 'json', async: false, success: function(json) {
		files_list = json;
	} });
	if (files_list == null || files_list.length < 1) {
		result.status = false;
		return result;
	}
	result.status = true;
	for (var f in files_list) {
		var file_name = files_list[f];
		//$('.messages').fadeIn(300);
		$('.messages').show(0);
		$('.messages .inner').html('<p>Traitement : ' + file_name + '</p>');
		jQuery.ajax({url: 'callbacks/set_watermark.php', datatype: 'json', async: false, data: {'file_name': file_name, 'text': watermark_text}, success: function(json) {
			//json = jQuery.parseJSON(json);
			if (json == false || json == undefined || json == null || json == '') {
				result.status = false;
			}
		} });
	}
	$('#preview_link').attr('href', 'http://cdn.pingveno.net/file-upload/watermark/preview/?album=' + encodeURIComponent(album_name));
	$('.messages .inner').html('');
	$('.messages').fadeOut(300);
	return result;
};

setInterval(function() {
	jQuery.get('callbacks/keepalive.php');
}, (1000 * 60 * 5)); // 5 minutes

