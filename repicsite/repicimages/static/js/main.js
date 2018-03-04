
$(document).ready(function() {
    
    function check(element) {
      if (element.is('input')) {
        if (element.checked == false) {
          element.checked = true;
        } else {
          element.checked = false;
        }
      } else {
        var subreddit = element.find('input')[0];
        if (subreddit.checked == false) {
          subreddit.checked = true;
        } else {
          subreddit.checked = false;
        }
      }
    }
    function highlight(element) {
      if (element.is('div')) {
        element.toggleClass('clicked');
      } else {
        var p = element.parent().closest('div');
        p.toggleClass('clicked');
      }
    }

    $('.subreddit').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        highlight($(this));
        check($(this));
    });
});
