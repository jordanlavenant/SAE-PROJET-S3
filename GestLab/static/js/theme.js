if (localStorage.getItem("theme")) {
    document.body.classList.add(localStorage.getItem("theme"));
} else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.body.classList.add("dark");
}

/**
 * Bascule le thème de la page web entre "dark" et "default".
 * Met à jour le thème dans le stockage local et envoie une requête AJAX pour mettre à jour le thème sur le serveur.
 */
function toggleTheme() {
    const body = document.body;

	if (body.classList.toggle("dark")) {
		applyTheme("dark");
		localStorage.setItem("theme", "dark");
		url_redirection = "/update-theme/0";
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


/**
 * Applique le thème spécifié au corps du document.
 * @param {string} theme - Le thème à appliquer.
 */
function applyTheme(theme) {
    const body = document.body;
    body.className = theme;
}