// some visual corrections
$(window).resize(function() {
	if ($(window).width() < 559) {
		$('#username').addClass('text-center');

		$('#user-img').removeClass('w-100');
		$('#user-img').addClass('w-75');

	} else {
		$('#username').removeClass('text-center');
		
		$('#user-img').removeClass('w-75');
		$('#user-img').addClass('w-100');
	};
});

$(document).ready(function() {
	if ($(window).width() < 559) {
		$('#username').addClass('text-center');

		$('#user-img').removeClass('w-100');
		$('#user-img').addClass('w-75');
	} else {
		$('#username').removeClass('text-center');

		$('#user-img').removeClass('w-75');
		$('#user-img').addClass('w-100');
	};
});