/*
Javascript file for assessment related activity
Author:"Sonali Kakade"
*/

// Page ready function
$(document).ready(function(){
  var qid = $('#question_id').val();
  var answer = $.jStorage.get(qid);
  answer = $.parseHTML( answer );
  $('#user_answer').append( answer );
});
