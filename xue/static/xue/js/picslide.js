(function($){
  // global "constants"
  var target_sel='.picslide_target',
      pool_sel='.picslide_pool',
      poolimg_sel=pool_sel + '>img',
      piclist_sel=target_sel + '>.picslide_piclist',
      piclist_selected_cls='picslide_selected',
      frame_duration_ms=8000,
      transition_ms=1000,
      left_attr='left',

      // state info
      cont_width,
      num_frames,

      // 0-based
      curr_frame,
      prev_frame,

      // element references
      $target,
      $pool,
      $imgs,
      piclist_elems,

      // handle of slide timer
      timer_id,
      slide_timer,

      // Page Visibility API support
      // https://developer.mozilla.org/en-US/docs/DOM/Using_the_Page_Visibility_API
      // Set the name of the hidden property and the change event for
      // visibility
      // FIXME: Get rid of most detection code once Modernizr builder
      // supports the 'pagevisibility' check!
      hidden,
      visibilityChange;


  if (typeof document.hidden !== "undefined") { // Opera 12.10 and Firefox 18 and later support
    hidden = "hidden";
    visibilityChange = "visibilitychange";
  } else if (typeof document.mozHidden !== "undefined") {
    hidden = "mozHidden";
    visibilityChange = "mozvisibilitychange";
  } else if (typeof document.msHidden !== "undefined") {
    hidden = "msHidden";
    visibilityChange = "msvisibilitychange";
  } else if (typeof document.webkitHidden !== "undefined") {
    hidden = "webkitHidden";
    visibilityChange = "webkitvisibilitychange";
  }


  function moveToFrame(idx)
  {
    // console.log('move to frame #' + idx);
    $pool.animate({left: -(cont_width * idx)}, transition_ms, postSliding);
  }

  function postSliding()
  {
    // rollover
    if (curr_frame == num_frames) {
      // console.log('roll over');
      $pool.stop().css(left_attr, 0);
      curr_frame = 0;
    }

    // update selected status
    if (prev_frame != curr_frame) {
      // current pic changed
      piclist_elems[prev_frame].toggleClass(piclist_selected_cls);
      piclist_elems[curr_frame].toggleClass(piclist_selected_cls);
    } else {
      // previous frame is the same!
      // this may result from the initial slide, or the user must had
      // clicked the same button >= 2 times
      piclist_elems[curr_frame].hasClass(piclist_selected_cls)
        ? 0 : piclist_elems[curr_frame].toggleClass(piclist_selected_cls);
    }
  }

  function cancelSlideTimer()
  {
    if (timer_id !== null) {
      clearTimeout(timer_id);
      timer_id = null;
    }
  }

  function doSlide(frameNr)
  {
    prev_frame = curr_frame;
    if (frameNr !== undefined) {
      // console.log('doSlide: frameNr=' + frameNr.toString());
      curr_frame = frameNr;
    } else {
      // console.log('doSlide: timer triggered');
      curr_frame++;
    }

    moveToFrame(curr_frame);

    cancelSlideTimer();
    timer_id = setTimeout(doSlide, frame_duration_ms);
  }

  function constructPicList(num_frames)
  {
    var list_tgt, tmp, i;

    list_tgt = $(piclist_sel);

    piclist_elems = new Array(num_frames);
    for (i=0;i<num_frames;i++) {
      tmp = $('<li />')
          .text((i + 1).toString())
          .click((function(idx){
            // must freeze the i in yet another level of closure
            return (function(){
              // terminate ongoing transition timer
              cancelSlideTimer();
              doSlide(idx);
            });
          })(i));
      piclist_elems[i] = tmp;
      list_tgt.append(tmp);
    }

    // "select" the first button
    piclist_elems[0].addClass(piclist_selected_cls);
  }

  function onVisibilityChange() {
    if (document[hidden]) {
      // don't slide the pictures if the user can't see it
      cancelSlideTimer();
    } else {
      cancelSlideTimer();
      timer_id = setTimeout(doSlide, frame_duration_ms);
    }
  }


  $(document).ready(function(){
    $target = $(target_sel);
    $pool = $(pool_sel);
    $imgs = $(poolimg_sel);

    cont_width = $target.width();
    num_frames = $imgs.length;
    curr_frame = 0;

    // nothing meaningful to do if there is only one picture
    if (num_frames > 1) {
      // for the smooth rollover effect, we fake the "first" image
      $pool.append($imgs.first().clone());
      // reload $img content
      $img = $(poolimg_sel);
      // picture list
      constructPicList(num_frames);

      timer_id = setTimeout(doSlide, frame_duration_ms);
    }

    // set up handler for Page Visibility API
    if (typeof document.addEventListener === "undefined" ||
        typeof hidden === "undefined") {
      // either addEventListener or Visibility API is not supported
    } else {
      // Handle page visibility change  
      document.addEventListener(visibilityChange, onVisibilityChange, false);
    }
  });
})($jq);


// vi:ai:et:ts=2:sw=2:sts=2:ff=unix:fenc=utf8:
