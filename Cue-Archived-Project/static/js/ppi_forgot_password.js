$(document).ready(function() {
    $("#recover-password").click(function() {
        var email = $("#id_email").val();
        var csrftoken = getCookie('csrftoken');
        email_inactive_verify(email, csrftoken);
    });
});

function email_inactive_verify(email, csrftoken) {
    $.ajax({
        url: "/auth/verify/email/",
        type: "POST",
        data: {
            email: email
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            console.log(response)
            if (response.indexOf("success") >= 0){
                $("#forgot-password").submit();
            }else{
                $(".panel-body").html("<centre>"+response+"</centre>");
            }
        },
    });
};
