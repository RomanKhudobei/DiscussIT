$(document).ready(function() {
	/* Highlight title after clicking side menu
	if (window.location.href.search('#') >= 0) {
		var id = '#' + window.location.href.split('#')[1];
		$(id).css('background-color', '#E3C381');
	}*/

	switch (window.location.pathname) {
		case '/api/docs/':
			$('[data-target=general]').addClass('active');
			break

		case '/api/docs/boards/':
			$('[data-target=boards]').addClass('active');
			break

		case '/api/docs/topics/':
			$('[data-target=topics]').addClass('active');
			break

		case '/api/docs/posts/':
			$('[data-target=posts]').addClass('active');
			break
	}
})


var target = $('#sidebar-nav')
target.after('<div class="affix" id="affix"></div>')

var affix = $('.affix')
affix.append(target.clone(true))

// Show affix on scroll.
var element = document.getElementById('affix')
if (element !== null) {
  var position = target.position()
  window.addEventListener('scroll', function () {
    var height = $(window).scrollTop()
    if (height > 170 && $(window).width() > 1000) {
      target.css('visibility', 'hidden')
      affix.css('display', 'block')
    } else {
      affix.css('display', 'none')
      target.css('visibility', 'visible')
    }
  })
}