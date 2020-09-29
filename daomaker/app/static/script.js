function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$(document).ready(function() {
    $('#TaskTable').DataTable();

    var success = $("#success")
    var error = $("#error")

    function submitForm() {
        var attachments = new FormData()
        var url = $("#InputUrl").val()
        attachments.append("url", url)

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });

        $.ajax({
            type: 'POST',
            url: '/',
            data: attachments,
            processData: false,
            contentType: false,
            async: false,
            success: function (data) {
                if (data === "success") {
                    success.slideDown()
                    error.hide()
                    $("#InputUrl").val("")
                    setTimeout(function(){
                        success.slideUp();
                    }, 3000);
                } else if (data === "url not valid") {
                    success.slideUp()
                    error.slideDown().html("The URL you provided is not valid")
                    $("#InputUrl").val("")
                    setTimeout(function(){
                        error.slideUp();
                    }, 3000);
                } else {
                    success.slideUp()
                    error.slideDown().html("There was an error while handling your request")
                    setTimeout(function(){
                        error.slideUp();
                    }, 3000);
                }
            },
            error: function (e) {
                console.log(e)
                success.slideUp()
                error.slideDown().html("There was an error while handling your request")
                setTimeout(function(){
                    error.slideUp();
                }, 3000);
            }
        })
    }

    $("#urlParseForm").submit(function(event) {
        event.preventDefault();
        submitForm();
    })

    $("#urlParseFormButton").click(function () {
        submitForm();
    })
})
