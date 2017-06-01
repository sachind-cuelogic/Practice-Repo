$(document).ready(function() {
    var working = false;
    var question_id = $(".form-control-comment").attr("id");
    question_reviews(question_id);
    $('#need_button').html('<a href="' + $('#next').val() + '" class="btn btn-primary">Back</a>');

    $(function() {
        $("#id_categories").autocomplete({
            source: "/knowledgebase/api/categories/list/",
            minLength: 0,
        });
    });

    $(function() {
        $("#id_topics").autocomplete({
            source: "/knowledgebase/api/topics/list/",
            minLength: 0,
        });
    });

    $('#addCommentForm').submit(function(e) {
        e.preventDefault();
        var note = $(".form-control-comment").val();
        if (note) {
            if (working) return false;

            working = true;
            $('#submit').val('Working..');
            $('span.error').remove();

            var question_id = $(".form-control-comment").attr("id");
            $('.form-control-comment').val('');
            $.ajax({
                url: "/knowledgebase/question/review/note",
                type: "GET",
                data: {
                    note: note,
                    question_id: question_id,
                },
                success: function(response) {
                    working = false;
                    $('#submit').val('Add');
                    $('.form-control-comment').val('');

                    if (response != 'Failed') {
                        var len = response.length;
                        var loggedin_user = $("#session_user").attr("value")

                        $('.commentList').last().append(response);

                        $('.commentList').animate({
                            scrollTop: $(document).height()
                        }, 'slow');

                    } else {
                        $('#comment-error').html(
                            '<b>' +
                            'You cannot add Comment before saving</b>');
                        $('#comment-error').css('color', 'red');
                    }
                }

            });
        }
    });
});

function question_reviews(question_id) {
    $.ajax({
        url: "/knowledgebase/question/reviews",
        type: "GET",
        data: {
            question_id: question_id
        },
        success: function(response) {
            if (response != 'Failed') {
                var len = response.length;
                var loggedin_user = $("#session_user").attr("value")
                $('.commentList').last().append(response);

                $('.commentList').animate({
                    scrollTop: $(document).height()
                }, 'slow');


            }

        }
    });
}


$('textarea').each(function() {
    var readonly = $(this).attr("readonly");
    if (readonly && readonly.toLowerCase() !== 'false') { // this is readonly
        tinymce.init({
            plugins: "noneditable",
            noneditable_leave_contenteditable: true
        });
        var text_id = $(this).attr('id');
        if (text_id == 'id_question') {
            $('#question').html('<p>' + $(this).val() + '</p>')
        }
        if (text_id == 'id_answer') {
            $('#answer').html('<p>' + $(this).val() + '</p>')
        }
        $('button[type="submit"]').hide()
        $(this).hide()
        if ($(this).attr('value') == 'save') {
            $(this).show()
        }
    } else {
        tinymce.init({
            selector: 'textarea[id="id_question"], textarea[id="id_answer"]'
        });
    }
});
$(function() {
    $('#deletesuccess').delay(5000).fadeOut();
});

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

$(".unflag").click(function() {
    unflag_question();
});

function unflag_question(flag_status) {
    var question_id = $(".form-control-comment").attr("id");
    $.ajax({
        url: "/knowledgebase/question/unflag",
        type: "GET",
        data: {
            question_id: question_id
        },
        success: function(response) {
            $("#flags-message").addClass("alert alert-success").text(response[0].message).delay(4000).fadeOut();
            $("#popup").hide();
        }
    });
}

$("#delete-question").click(function() {
    var question_id = $(".form-control-comment").attr("id");
    $.ajax({
        url: "/knowledgebase/question/delete/",
        type: "GET",
        data: {
            question_id: question_id
        },
        success: function(response) {
            var redirect = $('#next').val();
            window.location.href = redirect;
        }
    });
});
