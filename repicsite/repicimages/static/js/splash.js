
$(document).ready(function() {
  $('#nsfw-form').click(function(e) {
      e.stopPropagation();
      window.open("/nsfw", "_self");
  })
});