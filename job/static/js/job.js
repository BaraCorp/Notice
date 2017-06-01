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
    });

    $('.datetimepicker').datetimepicker({
        Default: new Date(),
        language:  'fr',
        format: 'dd/mm/yyyy hh:ii',
        weekStart: true,
        todayBtn:  true,
        autoclose: true,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: false,
        pickerPosition: "top-left"
    });

    $('.datepicker').datetimepicker({
        Default: new Date(),
        language:  'fr',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0
    });
})