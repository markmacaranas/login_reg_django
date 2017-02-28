$(document).ready(function(){
  $("input:not('.button')").focusin(function() {
    $(this).css("color","black");
    if($(this).val() == $(this).attr('default')) {
      $(this).val("");
    }
  });
  $("input:not('.button')").focusout(function() {
    if($(this).val() == "") {
      $(this).val($(this).attr('default'));
      $(this).css("color","#DDDDDD");
    }
  });
});
