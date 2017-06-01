$(document).ready(function() {
    $(".flag").click(function() {
        $('input[name="optradio"]').prop('checked', false);
        $(".textarea-hide").hide();
        $(".dynamic").attr("disabled", "");
        flag_remaining_check();
    });
    $(".radio-1").click(function() {
        $(".textarea-hide").hide();
    });

    $(".radio-2").click(function() {
        $(".textarea-hide").hide();
    });

    $(".radio-3").click(function() {
        $(".textarea-hide").hide();
    });

    $(".radio-text").click(function() {
        $(".textarea-hide").show();
    });

    $(".dynamic").click(function() {
    flag_question();
});

$(".all-tags").hide();

$(".view_link").click(function() {
    question_id = $(this).attr("id");
    panel = question_id.replace("link", "demo");
    link_text = $("#" + question_id + ".view_link").text();
    if (link_text == "VIEW ANSWER") {
        $("#" + question_id + ".view_link").text("HIDE ANSWER");
        $("#" + panel).show();
    } else {
        $("#" + question_id + ".view_link").text("VIEW ANSWER");
        $("#" + panel).hide();
    }
});

$(".view_tags").click(function(){
    q_id = $(this).attr("id");
    panel = q_id.replace("taglink", "questiontags");
    link_text = $(this).text();
    if (link_text == "View more"){
        $("#"+q_id).text("View less");
        $("#"+panel).show();
    }
    else{
        $("#"+q_id).text("View more");
        $("#"+panel).hide();
    }
});
});



function flag_question() {
    flag_message = ""
    question_id = $('input[name=optradio]:checked').attr('id');
    radio_class = $('input[name=optradio]:checked').attr('class');
    selected_radio_button = radio_class.replace("radio", "label");
    selected_radio_button = selected_radio_button + '-' + question_id;

    if (radio_class == "radio-text") {
        selected_radio_button = selected_radio_button.replace("text", "4");
        flag_message = $("#" + selected_radio_button).next().val();
    }
    flag_text = $("#" + selected_radio_button + " b").text();

    $.ajax({
        url: "/knowledgebase/question/flag/",
        type: "GET",
        data: {
            flag_text: flag_text,
            flag_message: flag_message,
            question_id: question_id
        },
        success: function(response) {

            if (response[0].message.indexOf("already") > -1) {
                $("#flag-notification-" + response[0].id).addClass("alert alert-danger");
                $("#flag-notification-" + response[0].id).html(response[0].message).show().delay(4000).fadeOut();
            } else {
                $("#flag-notification-" + response[0].id).addClass("alert alert-success");
                $("#flag-" + response[0].id).html("<b>Flagged</b>");
                $("#flag-notification-" + response[0].id).html(response[0].message).show().delay(4000).fadeOut();
            }
        },
    });
}

/* Centre Modal */
function centerModals($element) {
    var $modals;
    if ($element.length) {
        $modals = $element;
    } else {
        $modals = $('.modal-vcenter:visible');
    }
    $modals.each(function(i) {
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top);
    });
}
$('.modal-vcenter').on('show.bs.modal', function(e) {
    centerModals($(this));
});
$(window).on('resize', centerModals);

var $radioButtons = $("input:radio");

$radioButtons.change(function() {
    var anyRadioButtonHasValue = false;

    $radioButtons.each(function() {
        if (this.checked) {
            anyRadioButtonHasValue = true;
            return false;
        }
    });

    if (anyRadioButtonHasValue) {
        $(".dynamic").removeAttr("disabled");
    } else {
        // else is kind of redundant unless you somehow can clear the radio button value
        $(".dynamic").attr("disabled", "");
    }
});

function flag_remaining_check() {
    $.ajax({
        url: "/knowledgebase/question/flag/quantity/",
        type: "GET",
        data: {

        },
        success: function(response) {
            if (response >= 3) {
                $(".total-flags").text("Sorry you have no flags remaining");
                $(".dynamic").hide();
            } else {
                remaining_flag = 3 - response; 
                $(".total-flags").text("You have " + remaining_flag + " flags remaining");
            }
        },
    });
}
