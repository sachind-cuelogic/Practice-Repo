/*
Javascript file for assessment related activity
Author:"Sonali Kakade"
*/

// Page ready function
$(document).ready(function() {
    var qid = $('#question_id').val();
    var answer = $.jStorage.get(qid);
    $('#answer').val(answer);
});

// Initiating text area for answer
$('textarea').each(function() {
    tinymce.init({
        selector: 'textarea'
    });
});

// On Submit answer 
$("#subans").click(function(event) {
    var answer = tinyMCE.get('answer').getContent();
    var qid = $('#question_id').val();
    if (answer === '') {
        $("#no-answer-error").text("Answer can't be blank");
        $("#no-answer-error").css("display", "block").delay(3000).fadeOut();
        event.preventDefault();
        return 'Error';
    }
    $.jStorage.set(qid, answer);
});

// Reset page
$("#Reset").click(function() {
    tinymce.get('answer').setContent('');
    tinymce.get('answer').focus();
});
