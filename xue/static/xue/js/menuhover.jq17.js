// hover effect config
(function($){
  var hoverConfig = {
    over: function()
    {
      $(this).addClass("hover");
      //$("ul", this).show(200);
      return this;
    },
    out: function()
    {
      $(this).removeClass("hover");
      //$("ul", this).hide(200);
      return this;
    },
    timeout: 200
  };

  // set the hovering up
  function initHovers()
  {
    // 1st hide all submenus for nav_horiz
    $(".nav_left .submenu").hide();
    $(".nav_left li").hoverIntent(hoverConfig);
    $(".nav_horiz li").hoverIntent(hoverConfig);
    $(".developers").hoverIntent(hoverConfig);
  }

  // ready handler
  $(document).ready(function(){
    //initHovers();
  });
})($jq17);