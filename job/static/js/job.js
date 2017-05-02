$(document).ready(function(){
    $(".readMore").click(function(){
    var This=$(this);
    $(this).next().toggle(function(){
        if(This.text()=="Read"){
          This.text("Hide")
        }
        else{
            This.text("Read")
        }
    })
});})