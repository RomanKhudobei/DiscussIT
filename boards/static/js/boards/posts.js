// corrects user image size by changing padding
$(window).resize(function() {
	if ($(window).width() < 768) {
		$.each($('img').parent(), function() {
			$(this).addClass('px-2')
		});
	} else {
		$.each($('img').parent(), function() {
			$(this).removeClass('px-2')
		});
	};
});

$(document).ready(function() {
	if ($(window).width() < 768) {
		$.each($('img').parent(), function() {
			$(this).addClass('px-2')
		});
	} else {
		$.each($('img').parent(), function() {
			$(this).removeClass('px-2')
		});
	};
});