$(document).ready(function(){
    $(".line").width($("#all").width());
    $("#nedone").click(function() {
        $(this).css("color", "#0075FF")
        $("#all").css("color", "#000")
        $(".line").width($("#nedone").width()).css("transform", "translateX(10.4vw)");
        $("#tasks").css("transform", "translateX(-100%)");
    });
    $("#all").click(function() {
        $(this).css("color", "#0075FF")
        $("#nedone").css("color", "#000")
        $(".line").width($("#all").width()).css("transform", "translateX(2.8vw)");
        $("#tasks").css("transform", "translateX(0%)");
    });
});