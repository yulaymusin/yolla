function createCookie(name, value, days) {
	var expires;
	if (days) {
		var date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		expires = "; expires=" + date.toGMTString();
	} else {
		expires = "";
	}
	document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/; SameSite=Lax";
}
function eraseCookie(name) {
	createCookie(name, "", -1);
}
function changeTheme(themeName) {
	if ( themeName == "dark" ) {
		createCookie("theme", "dark");
		$("body").addClass("dark");
	} else {
		eraseCookie("theme");
		$("body").removeClass("dark");
	}
}
function readableFileSize(_size) {
	var fSExt = new Array('Bytes', 'KB', 'MB', 'GB');
	i=0;while(_size>900){_size/=1000;i++;}
	return (Math.round(_size*100)/100).toFixed(1)+' '+fSExt[i];
}
$(document).ready(function() {
	var current_uri = window.location.pathname;

	if (current_uri.indexOf('/participants/signup')+1) {
		$("#time_zone").val(Intl.DateTimeFormat().resolvedOptions().timeZone);
	}

	if (current_uri.indexOf('/opinions/attach_documents')+1) {

		document.querySelector('#attach_documents').addEventListener('change', function(evt) {
			$('#loading_bar').hide();
			$('#attach_btn').hide();
			$('#attach_documents_error').hide();
			var files = evt.target.files;
			var documents_list = [];
			var error = false;
			var allowed_filename_extensions = $('#attach_documents').attr('accept').split(',');
			var documents_length = $('#documents li').length;
			var f_max_size = $('#attach_documents_error').attr('f_max_size');
			var f_max_total = $('#attach_documents_error').attr('f_max_total');
			for (var i = 0, f; f = files[i]; i++) {
				var f_name_ext = '.' + f.name.toLowerCase().split('.').slice(-1);
				documents_length = documents_length + 1;
				if (f.size >= f_max_size || $.inArray(f_name_ext, allowed_filename_extensions) === -1 || documents_length > f_max_total) {
					documents_list.push('<li class="text-danger">');
					error = true;
				} else {
					documents_list.push('<li>');
				}
				documents_list.push('<b dir="auto">', f.name, '</b> [<bdi>', readableFileSize(f.size), '</bdi>, <bdi>"', f.type || 'n/a',
									'"</bdi>]</li>');
			}
			$('#documents_list').html('<ul>' + documents_list.join('') + '</ul>');

			if (error == false) {
				$('#attach_btn').show();
			} else {
				$('#attach_documents_error').show();
			}
		}, false);

		document.querySelector('#attach_btn').addEventListener('click', function() {
			if (document.querySelector('#attach_documents').files.length == 0) {
				alert('Error: No file selected');
				return;
			}

			$('#loading_bar').show();
			let loading_bar = $('#loading_bar div.bar');

			let data = new FormData();

			var documents_to_attach = document.getElementById('attach_documents').files.length;
			for (var x = 0; x < documents_to_attach; x++) {
				data.append("documents[]", document.getElementById('attach_documents').files[x]);
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
					var documents_list = [];
					var delete_word = $('#attach_documents_error').attr('delete');
					for (var i = 0, f; f = response[i]; i++) {
						documents_list.push('<li><a href="', f.url, '" target="_blank" dir="auto">', f.name, '</a> [<bdi>',
											readableFileSize(f.size), '</bdi>] (<a href="', f.delete_url, '">', delete_word, '</a>)</li>');
					}
					$('#documents ul').html(documents_list.join(''));
				}
				$('#attach_btn').hide();
				loading_bar.css({'width': '100%'}).addClass('success').removeClass('danger warning secondary primary');
			});

			request.send(data);
		});

	}
});