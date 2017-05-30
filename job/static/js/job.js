$(document).ready(function(){
    $(".readMore").click(function(){
    var This=$(this);
    $(this).next().toggle(function(){
        if(This.text()=="Lire la suite"){
          This.text("Fermer")
        }
        else{
            This.text("Lire la suite")
        }
    })
});})