$(document).ready(function() {
    $(".add-reminder").on("click", function() {
        var scope = $(this).closest(".patient-info");
        console.log(scope.find(".id").text());
        // MAKE AJAX REQUEST, GET NEXT APPOINTMENT (ERROR IF NOT) AND 
        // FILL OUT INFO FOR POST REQUEST
    });
});
