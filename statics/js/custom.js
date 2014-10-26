$(document).ready(function(){
  $('.list-group-item').click(function(){
    var email = $(this).children('p').text();

    // AJAX call 
    $.getJSON('get_user_json?email='+email, function(data) {
      $('#inputEmail').attr('value', data.email);
      $('#inputName').attr('value', data.name);
      $('#inputPassword').attr('value', data.password);
    });

  });
});