
function displayoverlay(){
    var article_form_container = document.querySelector(".article-form-container")
    var overlay = document.querySelector(".overlay")
    var Article_form = document.querySelector(".Article-form")
    if (overlay.style.display=="none") {
        overlay.style.display="block"
        article_form_container.style.display="block"
        article_form_container
        
    } else {
        overlay.style.display="none"
        article_form_container.style.display="none"
        
    }

    window.onclick = function(event) {
        if (event.target == overlay) {
          overlay.style.display = "none";
          article_form_container.style.display="none"
        }else if (article_form_container.style.display=="none"){
            article_form_container.style.display="none"
            overlay.style.display = "none";

        }
        

      }
}
