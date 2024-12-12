$(function () {

    jQuery('[data-bs-toggle="tooltip"]').tooltip();
    jQuery('[data-bs-toggle="modal"][title]').tooltip();


});


// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

/**
 * copy link url current window
 */
const btnCopy = document.querySelector(".btnCopy");
if (btnCopy){
    btnCopy.addEventListener("click",()=>{
        navigator.clipboard.writeText(window.location.href);
        alert("لینک کپی شد")
    })
}

