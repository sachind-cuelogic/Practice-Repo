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
$(function() {
  $("#id_Category ").change(
    function(event){
      event.preventDefault();
      var str=[];
      var csrftoken = getCookie('csrftoken');
      $( "#id_Category option:selected" ).each(function() {
        str.push($(this).val());
      });
      $.ajax({
        url: "/knowledgebase/api/search/topics/",
        type: "POST",
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }, 
        data:{category_id:str},
        success:
          function(response){
            $('#id_Topic').html(response);
            $("#id_Topic").multiselect("destroy");
            $('#id_Topic').multiselect({
                includeSelectAllOption: true,
                enableFiltering: true,
                enableCaseInsensitiveFiltering: true
            });
        },
        error:
          function(response){
            $('#id_Topic').html(response);
          },
      });
    }
  );
});
function getsearchvalue(str){
  $("#search_query").val(str);
}
$(document).ready(function() {
   $('#id_Category').multiselect({
          includeSelectAllOption: true,
          enableFiltering: true,
          enableCaseInsensitiveFiltering: true
      });
    $('#id_Topic').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
    $('#id_Difficulty').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
});
