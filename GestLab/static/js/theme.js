if (localStorage.getItem("theme")) {
    document.body.classList.add(localStorage.getItem("theme"));
} else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.body.classList.add("dark");
}

function toggleTheme(userId) {
	console.log(userId);
    const body = document.body;
	const url = "/update-theme/" + userId;

    if (body.classList.toggle("dark")) {
        applyTheme("dark");
        localStorage.setItem("theme", "dark");
		$.ajax({
			url: url,
			type: 'POST',
			success: function(response) {
				console.log(response);
			}
		});
    } else {
        applyTheme("default");
        localStorage.setItem("theme", "default");
    }
}


function applyTheme(theme) {
    const body = document.body;
    body.className = theme;
}