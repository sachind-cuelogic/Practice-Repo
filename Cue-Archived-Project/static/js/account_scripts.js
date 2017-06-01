$("#notificationLink").click(function()
{
    var user_id = $('input[id="user_id"]').val();
    get_notifications(user_id)
    set_notifications_as_notified(notification_ids)
$("#notificationContainer").fadeToggle(300);
$("#notification_count").fadeOut("slow");
    set_notifications_as_notified(notification_ids)
return false;
});

$("#notificationFooter a").click(function()
{
    var user_id = $(this).attr('href');
    window.location.href = $(this).attr("href");
});

//Document Click
$(document).click(function()
{
$("#notificationContainer").hide();
});
//Popup Click
$("#notificationContainer").click(function()
{
return false
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function get_notifications(u_id) {
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url : "/knowledgebase/api/notifications/get/", // the endpoint
        type : "POST", // http method
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data : { user_id : $('input[id="user_id"]').val() }, // data sent with the post request
        // handle a successful response
        success : function(response) {
            $('#ajax-notification').html('');
            $.each(response, function(i, jsonobjectlist) {
                if(jsonobjectlist.viewed == false){
                  str ='<li class="not-viewed-notifications">'
                }
                else{
                  str = '<li>'
                }
                str1 =   '<div id="notification-text">\
                          <a href="'+jsonobjectlist.link+'&notification_id='+jsonobjectlist.notification_id+'"> \
                            '+jsonobjectlist.notification_txt+' \
                          </a></div> \
                          <div id="notification-timestamp"> \
                            '+jsonobjectlist.timestamp+' \
                          </div> \
                         \
                      </li>';
                $('#ajax-notification').append(str+str1);
            });
            $('ul li [id="notification-text"] a').click(function(){
                    window.location.href = $(this).attr("href");
                });

        },
        error: function(response) {
                $('#resultdisplay').html("");
            },
        // handle a non-successful response
    });
};
function get_notifications_count(u_id) {
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url : "/knowledgebase/api/notifications/count/", // the endpoint
        type : "POST", // http method
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data : { user_id : $('input[id="user_id"]').val() }, // data sent with the post request
        // handle a successful response
        success : function(response) {
            $('#notification_count').html('');
            var count = response[response.length-1].count;
            if(count > 0)
            {
                $('.notify_me').html('<span id="notification_count" class="badge">'+response[response.length-1].count+'</span>');
            }
            window.notification_ids = response;

        },
        error: function(response) {
                $('#notification_count').html('');
            },
        // handle a non-successful response
    });
};

function set_notifications_as_notified(id_list) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : "/knowledgebase/api/notifications/notified/", // the endpoint
        type : "POST", // http method
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data : { 'notification_id_list' : JSON.stringify(id_list) }, // data sent with the post request
        // handle a successful response
        success : function(response) {
        },
        error: function(response) {
                $('#notification_count').html('');
            },
        // handle a non-successful response
    });
};

$( document ).ready(function() {
    var user_id = $('input[id="user_id"]').val();
    if(window.user_auth != "False"){
        get_notifications_count(user_id)
    }
});

