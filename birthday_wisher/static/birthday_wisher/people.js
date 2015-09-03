$(document).ready(function() {
    $(".add-reminder").on("click", function() {
        $(".alert-success").remove();
        var scope = $(this).closest(".patient-info");
        var patient_id = scope.find(".id").text();
        $.get("/next_appointment/" + patient_id, function(data) {
            if (!("scheduled_time" in data)) {
                $(".note-body").hide();
                $(".submit-note").hide();
                $(".note-date").text("This person has no appointments");
            }
            else {
                $(".note-body").show();
                $(".note-body").text(data["notes"]);
                $(".submit-note").show();
                $(".appt-id").val(data["id"]);
                $(".note-date").text(data['scheduled_time']);
            }
        });
    });

    $(".add-note").on("submit", function() {
        data = {
            "id":    $(".appt-id").val(),
            "notes": $(".note-body").val()
        };
        $.post("/add_note/", data, function (response) {
            $(".modal-body")
                .append("<span class='alert alert-success'>Note updated</span>");
        });
        return false;
    });
});
