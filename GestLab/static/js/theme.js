if (localStorage.getItem("theme")) {
    document.body.classList.add(localStorage.getItem("theme"));
} else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.body.classList.add("dark");
}

function toggleTheme() {
    const body = document.body;
	const param = document.querySelector('.theme').dataset.param;

	if (body.classList.toggle("dark")) {

		if (param == 1) {
			applyTheme("dark");
			localStorage.setItem("theme", "dark");
			url_redirection = "/update-theme/0";
		}
		
	}

	else {
		applyTheme("default");
		localStorage.setItem("theme", "default");
		url_redirection = "/update-theme/1";
	}

	$.ajax({
		url: url_redirection,
		type: 'GET',
		contentType: 'application/json',
		success: function(response) {
			console.log(response);
		},
	});
	
}


function applyTheme(theme) {
    const body = document.body;
    body.className = theme;
}

