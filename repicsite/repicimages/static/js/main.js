
$(document).ready(function() {
      function highlight(element) {
      if (element.is('li' || 'input')) {
        console.log('li')
        if (element.hasClass('clicked')) {
          element.removeClass('clicked');
        } else {
          element.addClass('clicked');
        }
        var subreddit = element.find('input')[0];
        if (subreddit.checked == false) {
          subreddit.checked = true;
        } else {
          subreddit.checked = false;
        }
      }
    }
    function highlight(element) {
      if (element.is('div' || 'li' || 'input')) {
        console.log('div')
        if (element.hasClass('clicked')) {
          element.removeClass('clicked');
        } else {
          element.addClass('clicked');
        }
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
});
