
$(document).ready(function() {

    function highlight(element) {
      if (element.is('div')) {
        if (element.hasClass('clicked')) {
          element.removeClass('clicked');
        } else {
          element.addClass('clicked');
        }
        console.log(element.find('input'[0]))
        var subreddit = element.find('input')[0];
        if (subreddit.checked == false) {
          subreddit.checked = true;
        } else {
          subreddit.checked = false;
        }
      }
    }

$('.subreddit').click(function(e) {
    highlight($(this));
    });

$(".subreddit li label input").click(function(e) {
    e.stopPropagation();
    highlight($(this).parent().parent());
   });


$('.gifplayer');
$('.gifplayer').gifplayer();

$gifs = $('.gif');

$gifs.each(function (i, gif) {
    $(gif).data('isPlaying', false);
});


$(window).scroll(function () {
    $gifs = $('.gif');

    $gifs.each(function (i, gif) {
        $gif = $(gif);

        if ($gif.visible(true)) {
            if (!$gif.data('isPlaying')) {
                $gif.find('.gifplayer').gifplayer('play');
                $gif.data('isPlaying', true);
            }

            if ($gif.find('.gp-gif-element').length > 1) {
                $gif.find('.gp-gif-element').first().remove();
            }
        } else {
            if ($gif.data('isPlaying')) {
                $gif.find('.gifplayer').gifplayer('stop');
                $gif.data('isPlaying', false);
            }
        }
    });
});
});
