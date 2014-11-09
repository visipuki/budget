$(document).ready(function() {
	$("td").each(function() {
		var value = parseInt($(this).html());
		if (value<0) {
			$(this).addClass("attention");
		}
	});
});
