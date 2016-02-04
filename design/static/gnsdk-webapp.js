function toggle_image(this_img) {
	
	if ($(this_img).attr('id') != 'artist-image')
	{
		if ($("#artist-image").hasClass('is-fullsize')) 
		{
			toggle_image($("#artist-image"));
		}
	}
	if ($(this_img).attr('id') != 'cover-art')
	{
		if ($("#cover-art").hasClass('is-fullsize')) 
		{
			toggle_image($("#cover-art"));
		}
	}
	if ($(this_img).attr('id') != 'genre-image')
	{
		if ($("#genre-image").hasClass('is-fullsize')) 
		{
			toggle_image($("#genre-image"));
		}
	}
		
	$(this_img).toggleClass('is-fullsize'); 
	if ($(this_img).hasClass('is-fullsize')) {
		$(this_img).attr('src', $(this_img).data('src-fullsize'));
	}
	else {
		$(this_img).attr('src', $(this_img).data('src-small'));
	}	
}

/*
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
  
});*/



// text input fields

function Resizer( element ) {

    var inputBox = element;
    var cssRules = window.getComputedStyle(inputBox);
    var maxFontSize = parseInt(cssRules.getPropertyValue("font-size"));
    var minFontSize = 11; // 11 is pretty damn small!
    var currentFontSize = maxFontSize;
    var maxScrollWidth = parseInt(cssRules.getPropertyValue("width"));
    var fontFamily = cssRules.getPropertyValue("font-family");
    var currentText = inputBox.value;

    // canvas used to check text widths.
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');

    var initialize = function() {

        inputBox.oninput = onUpdate;
    }

    var onUpdate = function(event) {

        var width;
        // some text has been deleted!
        if (inputBox.value.length < currentText.length) {
            width = checkTextWidth(inputBox.value, currentFontSize + 1);

            while (width < maxScrollWidth && currentFontSize < maxFontSize) {
                currentFontSize += 1;
                inputBox.style.fontSize = currentFontSize + 'px';
                width = checkTextWidth(inputBox.value, currentFontSize + 1);
            }

            currentText = inputBox.value;
            return;

        }

        var width = checkTextWidth(inputBox.value, currentFontSize);

        // minimize
        while (currentFontSize > minFontSize && width > maxScrollWidth) {
            currentFontSize -= 1;
            inputBox.style.fontSize = currentFontSize + 'px';
            width = checkTextWidth(inputBox.value, currentFontSize);
        }

        currentText = inputBox.value;
    }

    var checkTextWidth = function(text, size) {
        context.font = size + "px " + fontFamily;

        if (context.fillText) {
            return context.measureText(text).width;
        } else if (context.mozDrawText) {
            return context.mozMeasureText(text);
        }
    }

    // initialize auto adapt functionality.
    initialize();
}

Resizer( document.getElementById( 'resizer' ) );


