$(document).ready(function() {
    $(".request-result-btn").click(function() {
        $("#results").slideToggle(function() {
            if ($(this).is(":visible")) {
                localStorage.setItem("request-result", "opened")
            }
            else {
                localStorage.setItem("request-result", "closed")
            }
        });
    });

    let state = localStorage.getItem("request-result");
    if (state === "closed") {
        $("#results").hide();
    }
    else {
        $("#results").show();
    }
});