$('img').on('click', function() {

  $('li').toggleClass('is-fullsize'); 
  if($('.Wrapper').hasClass('is-fullsize')) {
     $.each($('img'), function() {
       $(this).attr('src', $(this).data('src-small'));
     });
  } else {
    $.each($('img'), function() {
      $(this).attr('src', $(this).data('src-fullsize'));
    });
  }
  $('.Wrapper').toggleClass('is-fullsize');
  
  // focus on clicked image
  $(document).scrollTop($(this).offset().top);
  
});