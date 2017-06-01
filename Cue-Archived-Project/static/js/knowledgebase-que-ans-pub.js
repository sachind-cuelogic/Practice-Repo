$(document).ready(function() {
    $("#nav li a").click(function() {
        var question_state = $(this).attr('href');
        window.location.href = question_state
    });
    $("input[type=submit]").on('click', function() {
        var question_id = $(this).attr('id')
        var question_state = $(this).val()
        var csrftoken = getCookie('csrftoken');
        question_publish(question_state, question_id, csrftoken);
    });
});

function question_publish(question_state, question_id, csrftoken) {
    $.ajax({
        url: "/knowledgebase/question/publish",
        type: "POST",
        data: {
            question_state: question_state,
            question_id: question_id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {

            button_id = 'que-ans-' + question_id

            if (response.indexOf("Published") >= 0) {
                $('#' + button_id).addClass("publish-question");
            } else {
                $('#' + button_id).addClass("reject-question");
            }
            $('#' + button_id).empty().text(response);
        },
    });
};
