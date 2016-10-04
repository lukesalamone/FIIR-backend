$(document).ready(function(){
	$("#fiir").click(function(){
		refresh("fiir");
	});
	$("#wild").click(function(){
		refresh("wild");
	});
	$("#vip").click(function(){
		refresh("vip");
	});
});

function refresh(section){
	var after = 0;	// todo
	$.ajax({
		url: 'process.php',
		type: 'post',
		data: {'action':'refresh', 'price':section, 'after':after},
		dataType: 'json',
		complete: function() {
			// do something
		},
		success: function(data) {
			console.log(data);
		},
		error: function() {
			// todo
		}
	});
}


