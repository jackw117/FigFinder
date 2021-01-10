$(document).ready(function() {
    var frm = $('#new-search');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $("#database").append(data);
                $("#modalClose").click();
                $("#noData").remove();
                checkLimit();
            },
            error: function(data) {
                $("#errors").html("Something went wrong!");
            }
        });
        return false;
    });

    $(document).on('submit', '.removeForm', function(e) {
        e.preventDefault()
        var remove = $(this).parent(".item");
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (data) {
                remove.remove();
                checkLimit();
            },
            error: function(data) {
                $("#errors").html("Something went wrong!");
            }
        });
        return false;
    });
});

function checkLimit() {
    if ($(".item").length == $("#limitSpan").text()) {
        $("#modalButton").prop("disabled", true);
    } else {
        $("#modalButton").prop("disabled", false);
    }
}