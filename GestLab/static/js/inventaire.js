const alerts = document.querySelectorAll('.alerts_count').forEach(alert => {
    let parent = alert;
    for (let i = 0 ; i < 5 ; i++) {
        parent = parent.parentElement;
    }
    parent.style.borderLeft = "15px solid #d35252";
});