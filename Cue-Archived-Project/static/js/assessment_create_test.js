/*
Javascript file for assessment related activity
Author:"Sonali Kakade"
*/

// Page ready function
$(document).ready(function() {
    $('#id_Topic').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
    $('.spinner input').keydown(function(e) {
        e.preventDefault();
        return false;
    });
    var minNumber = 0;
    $('.spinner .btn:first-of-type').on('click', function() {
        $('.spinner input').val(parseInt($('.spinner input').val(), 10) + 5);
    });

    $('.spinner .btn:last-of-type').on('click', function() {
        if ($('.spinner input').val() <= minNumber) {
            return false;
        } else {
            $('.spinner input').val(parseInt($('.spinner input').val(), 10) - 5);
        }
    });

    $("#practice_test").show();
    $("#mentor_test").hide();
    practice_test_button.style.background = "#98B2FF";
    mentor_test_button.style.background = "";

    $("#practice_test_button").click(function() {
        $("#practice_test").show();
        $("#mentor_test").hide();
        practice_test_button.style.background = "#98B2FF";
        mentor_test_button.style.background = "";
    });

    $("#mentor_test_button").click(function() {
        $("#practice_test").hide();
        $("#mentor_test").show();
        practice_test_button.style.background = "";
        mentor_test_button.style.background = "#98B2FF";
    });
    
});

//On Start test
$("#start_test").click(function(e) {
    var difficulties = []
    var topic_list = []
    var no_of_questions = parseInt($('.spinner input').val());
    var diff = $('.checkbox input').val();
    $.jStorage.flush();
    $('input[name="difficulty"]:checked').each(function() {
        difficulties.push(this.value);
    });
    $("#id_Topic option:selected").each(function() {
        topic_list.push($(this).val());
    });
    if (difficulties.length == 0 || no_of_questions == 0) {

        if (no_of_questions == 0) {
            $("#spinner_message").text("Sorry !!! Please Increase the Number of questions...");
            $("#spinner_message").css("display", "block").delay(3000).fadeOut();
        }
        if (difficulties.length == 0) {
            $("#difficulty_message").text("Sorry !!! Please Select the Difficulty Level...");
            $("#difficulty_message").css("display", "block").delay(3000).fadeOut();
        }
    } else {
        $.ajax({
            url: "/assessment/check/results/",
            type: "get",
            data: {
                category_id: $('#id_Category :selected').val(),
                topic_list: topic_list,
                difficulty: difficulties
            },
            success: function(response) {
                if (response == 0) {
                    $("#error_message").text("Sorry !!! No Questions Available... Please select again...");
                    $("#error_message").css("display", "block").delay(3000).fadeOut();
                } else {
                    $("#create_test").submit();
                }
            },
            error: function(response) {
                console.log(reponse);
            },
        });
    }
});
