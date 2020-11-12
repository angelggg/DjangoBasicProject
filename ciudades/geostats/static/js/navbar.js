function markActive(){
	var current_url =  "/" + new URL(window.location.href).pathname.split("/")[1];
	document.querySelectorAll('.nav-link').forEach(function(nav_button) {
		var split_url = new URL(nav_button.href).pathname.trim("/");
		console.log(split_url, current_url);
		if (split_url === current_url){
			nav_button.classList.add("active");
			nav_button.href = 'javascript:;';
		}
	});
	}


window.onload = markActive;