function convertToSlug(Text) {
	return Text.toLowerCase().replace(/[^a-zA-Z0-9]+/g,'-');
}
function getUrlParameter(sParam) {
	var sPageURL = window.location.search.substring(1),
		sURLVariables = sPageURL.split('&'),
		sParameterName,
		i;

	for (i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');

		if (sParameterName[0] === sParam) {
			return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
		}
	}
	return false;
}
function copyImageHTMLTagToClipboard(image_id) {
	$('#images a.tooltip.tip-top span.tip').html('Copy image HTML tag to clipboard');
	var copyText = document.getElementById("image_html_tag_"+image_id); /* Get the text field */
	copyText.select(); /* Select the text field */
	copyText.setSelectionRange(0, 99999); /* For mobile devices */
	document.execCommand("copy"); /* Copy the text inside the text field */
	var tooltip = document.getElementById("copy_img_tip_"+image_id); /* Alert the copied text */
	tooltip.innerHTML = "Copied: " + copyText.value.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;');
}
$(document).ready(function() {
	var current_uri = window.location.pathname;

	if ( (current_uri.indexOf('/categories/new')+1 || current_uri.indexOf('/categories/edit')+1
		|| current_uri.indexOf('/topics/new')+1 || current_uri.indexOf('/topics/edit')+1 )
		&& $('#id_slug').length && $('#id_slug').val().length == 0
	){
		$('#id_en_name').on('keyup', function() {
			$('#id_slug').val(convertToSlug($('#id_en_name').val()));
		});
	}

	if (current_uri.indexOf('/articles/upload_images')+1) {

		document.querySelector('#upload_images').addEventListener('change', function(evt) {
			$('#loading_bar').hide();
			$('#upload_btn').hide();
			$('#upload_images_error').hide();
			var files = evt.target.files;
			var images_list = [];
			var error = false;
			var allowed_filename_extensions = $('#upload_images').attr('accept').split(',');
			var f_max_size = $('#upload_images_error').attr('f_max_size');
			var f_max_total = $('#upload_images_error').attr('f_max_total');
			for (var i = 0, f; f = files[i]; i++) {
				var f_name_ext = '.' + f.name.toLowerCase().split('.').slice(-1);
				if (f.size >= f_max_size || $.inArray(f_name_ext, allowed_filename_extensions) === -1) {
					images_list.push('<li class="text-danger">');
					error = true;
				} else {
					images_list.push('<li>');
				}
				images_list.push('<b>', f.name, '</b> [', readableFileSize(f.size), ', "', f.type || 'n/a', '"]</li>');
			}
			$('#images_list').html('<ul>' + images_list.join('') + '</ul>');

			if (error == false) {
				$('#upload_btn').show();
			} else {
				$('#upload_images_error').show();
			}
		}, false);

		document.querySelector('#upload_btn').addEventListener('click', function() {
			if (document.querySelector('#upload_images').files.length == 0) {
				alert('Error: No file selected');
				return;
			}

			$('#loading_bar').show();
			let loading_bar = $('#loading_bar div.bar');

			let data = new FormData();

			var images_to_upload = document.getElementById('upload_images').files.length;
			for (var x = 0; x < images_to_upload; x++) {
				data.append("images[]", document.getElementById('upload_images').files[x]);
			}

			let request = new XMLHttpRequest();
			request.open('POST', current_uri);
			request.setRequestHeader('X-CSRFToken', $('#csrf_token').attr('value'));

			request.upload.addEventListener('progress', function(e) {
				let percent_complete = (e.loaded / e.total)*100;
				loading_bar.css({'width': percent_complete + '%'});
				if (percent_complete <= 10) {
					loading_bar.addClass('danger').removeClass('warning secondary primary success');}
				if (percent_complete <= 25 && percent_complete > 10) {
					loading_bar.addClass('warning').removeClass('danger secondary primary success');}
				if (percent_complete <= 50 && percent_complete > 25) {
					loading_bar.addClass('secondary').removeClass('danger warning primary success');}
				if (percent_complete <= 75 && percent_complete > 50) {
					loading_bar.addClass('primary').removeClass('danger warning secondary success');}
			});

			request.addEventListener('load', function(e) {
				if (request.status == 200) {
					var response = JSON.parse(request.response);
					var images_list = [];
					if ( getUrlParameter('list') != '1' ) {
						for (var i = 0, f; f = response[i]; i++) {
							images_list.push('<tr><td class="text-center"><a onclick="copyImageHTMLTagToClipboard(\'',
									f.id, '\');" class="tooltip tip-right">Copy image tag<span class="tip" id="copy_img_tip_',
									f.id, '">Copy image HTML tag to clipboard</span></a><br><a href="', f.del_url,
									'">Delete</a>', '</td><td><a href="', f.url, '" target="_blank">', f.name, '</a></td>',
									'<td class="text-center"><a href="', f.url, '" target="_blank"><img src="', f.url,
									'"></a></td>', '<td class="text-center">', readableFileSize(f.size), '</td>',
									'<td><input id="image_html_tag_', f.id, '" value="&lt;img src=&quot;', f.path,
									'&quot;&gt;"></td></tr>');
						}
						$('#images tbody').html(images_list.join(''));
					} else {
						for (var i = 0, f; f = response[i]; i++) {
							images_list.push('<li><a href="', f.url, '" target="_blank">', f.name, '</a> [',
									readableFileSize(f.size), '] (<a href="', f.del_url, '">', 'Delete', '</a>)</li>');
						}
						$('#images ul').html(images_list.join(''));
					}
				}
				$('#upload_btn').hide();
				loading_bar.css({'width': '100%'}).addClass('success').removeClass('danger warning secondary primary');
			});

			request.send(data);
		});

	}
});