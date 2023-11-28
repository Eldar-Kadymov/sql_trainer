$(document).ready(function() {
  $(".module").click(function() {
    $(this).next().slideToggle(function() {
      $(".task-list").each(function(i) {
        if ($(this).is(":visible")) {
          localStorage.setItem("task-list-" + i, "opened")
        }
        else {
          localStorage.setItem("task-list-" + i, "closed")
        }
      })
    });
    $(this).next().toggleClass("closed")
    if ($(this).next().hasClass("closed")) {
        $(this).find(".bxs-chevron-down").css("transform", "rotate(-90deg)")
    }
    else {
        $(this).find(".bxs-chevron-down").css("transform", "rotate(0deg)")
    }
  });


  $(".task-list").each(function(i) {
    var state = localStorage.getItem("task-list-" + i);
    if (state === "closed") {
      $(this).hide();
    }
    else {
      $(this).show();
    }
  })
});