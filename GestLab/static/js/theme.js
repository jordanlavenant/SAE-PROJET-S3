if (localStorage.getItem("theme")) {
    document.body.classList.add(localStorage.getItem("theme"));
} else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.body.classList.add("dark");
}

function toggleTheme(userId) {
	console.log(userId);
    const body = document.body;

    if (body.classList.toggle("dark")) {
        applyTheme("dark");
        localStorage.setItem("theme", "dark");
    } else {
        applyTheme("default");
        localStorage.setItem("theme", "default");
    }
}

function applyTheme(theme) {
    const body = document.body;
    body.className = theme;
}