document.getElementById("btn-send").addEventListener("click",function() {
    const text = document.getElementById("comment-wrapper").value;

    if(text != "") {
        document.getElementById("myPopup").style.display = "block";
        document.body.style.overflow = "hidden";
    }
});