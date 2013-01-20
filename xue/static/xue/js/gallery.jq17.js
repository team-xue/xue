(function($){
  // global vars and states
  var total_pics, // total number of <img>'s
      curr_idx, // current exhibiting <img>, 0-based
      thumb_leftmost, // the leftmost of currently displaying thumbs, 0-based
      num_thumb_exposed, // number of thumbnails that can be shown at a time
      thumb_center_idx, // the center position of thumblist..
                        // NOTE this is CONSTANT during runtime!!
      curr_thumb_idx, // current center position of thumb,
                      // initialized indirectly by doGotoPhoto(0, true)
      image_pool, // $ object of all <img>'s
      thumb_pool, // $ of all thumbnail <li>'s
      curr_idx_tag, // $ of span.curr tag
      target_photo_tag, // $ of div.photo img
      target_thumb_tag, // $ of div.thumbnails>ul
      photo_title_tag; // $ of div.perphoto div.metadata span.title

  // the vars are to help minification...
  var div_pres = '.presentation ',
      div_imag = '.imagelist ',
      div_pool = '.photopool ',
      div_prev = '.prev',
      div_next = '.next',
      div_thumb = '.thumbnails',
      cls_enabled = 'enabled',
      math_ceil = Math.ceil;

  function centerAlign(elem, overrideWidth, overrideHeight)
  {
    var parent = elem.parent(),
        top_offset,
        left_offset,
        // now the caller can override the dimension... just give a val >= 0
        e_hgt = (overrideHeight >= 0) ? overrideHeight : elem.height(),
        e_wdt = (overrideWidth >= 0) ? overrideWidth : elem.width(),
        p_hgt = parent.height(),
        p_wdt = parent.width();

    // calculate a top attr offset to accomplish vertical center alignment
    // but only if elem is not 0px-high (such as one tag that's not cleared)
    // AND parent has a non-zero dimension...
    if (e_hgt && p_hgt) {
      top_offset = (p_hgt - e_hgt) / 2;
      elem.css('top', top_offset.toString() + 'px');
    }

    // also a left offset... dunno why this can't be done using only CSS
    if (e_wdt && p_wdt) {
      left_offset = (p_wdt - e_wdt) / 2;
      elem.css('left', left_offset.toString() + 'px');
    }
  }

  // THUMBNAIL LIST OPERATIONS
  //
  function initThumbnails()
  {
    var container_width,
        elem_width,
        prev_thumb_btn = $(div_imag + div_prev),
        next_thumb_btn = $(div_imag + div_next);

    // first get and construct the ul
    target_thumb_tag = $(div_thumb + '>ul');

    image_pool.each(function(idx){
      // make a list item of one thumbnail
      var elem=$(this),
          // enabled by default...
          tmp_li = $('<li />', {'class': ('gal_btn ' + cls_enabled)}),
          tmp_div = $('<div />', {'class': 'thumb'});

      tmp_div.append(elem);
      tmp_li.append(tmp_div).appendTo(target_thumb_tag);

      // unfortunately, because the thumbnail list is now generated on the fly,
      // setting event handler here doesn't work anymore...
      // try to use some data-like approach.
      // the data is stored in <li>
      //
      // tmp_li.data(key_photoidx, idx);
      //
      // The data()-based approach won't work either... fall back to manually
      // figuring out the index.

      // center the image...      
      centerAlign(elem);
    });

    // second obtain dimensions and decide how many thumbs to display
    // XXX this code assumes all li's are equal in width,
    // taking the first one's as the measurement
    elem_width = target_thumb_tag.children().first().width();
    container_width = target_thumb_tag.width();

    // update global state
    num_thumb_exposed = math_ceil(container_width / elem_width);

    // must clone() here because of the slicing...
    thumb_pool = target_thumb_tag.children().clone();
    thumb_center_idx = math_ceil(num_thumb_exposed / 2);

    // center the imagelist
    // thx to the enhanced centerAlign, only horizontal dir. is centered
    // because the ul isn't cleared, hence height is 0px
    // here we enforce this 0px by explicitly overriding it
    // and the width MUST be "manually" calculated as well, or it stretches to
    // 100%...
    centerAlign(target_thumb_tag,
                // overrideWidth
                elem_width * (total_pics <= num_thumb_exposed
                  ? total_pics
                  : num_thumb_exposed
                  ),
                // overrideHeight
                0
                );

    // if total number of photos is less than number of thumbnails
    // that can be displayed at a time, disable scrolling altogether
    if (total_pics <= num_thumb_exposed) {
      // apply disable class
      prev_thumb_btn.toggleClass(cls_enabled);
      next_thumb_btn.toggleClass(cls_enabled);

      return;
    }

    // set up thumbnail
    // NOTE the initial arrangement is done in doGotoPhoto(0, true).

    // button event handlers
    prev_thumb_btn.click(prevThumbClicked);
    next_thumb_btn.click(nextThumbClicked);
  }

  function clickHandlerFactory(idx)
  {
    return function(){
      doGotoPhoto(idx);
    };
  }

  function arrangeThumbnails(idx)
  {
    // idx denotes the selected photo
    // its position should be at the center
    // if idx is at both edges, wraparound the list

    var new_leftmost, new_rightmost, photo_idx;

    // if there are too few photos, do not go any further
    if (total_pics <= num_thumb_exposed)
      return;

    // update current position...
    curr_thumb_idx = idx;

    // calculate the scope...
    // strangely there's a -1 offset...
    new_leftmost = idx - thumb_center_idx + 1;
    new_rightmost = new_leftmost + num_thumb_exposed;

    // prepare to replace the list...
    target_thumb_tag.empty();

    // only lookup the method once, both beneficial to performance (isn't the
    // "benefit" negligible??) and minification
    // XXX THIS IS NOT POSSIBLE BECAUSE JQUERY WOULD BREAK IF WE TRY THIS WAY
    // I don't know the reason, but keep this line for a good lesson...
    //poolSlice = thumb_pool.slice;

    // in the normal case when total_pics > num_thumb_exposed
    // (though the thumbnail-related funcs will not trigger if it's not the
    // case), only one side if any can wrap to the other side,
    // so we can detect the two cases separately.

    // scroll toward the left and wrap
    if (new_leftmost < 0) {
      // -new_leftmost is the number of images actually wrapped around
      // slices: [new_leftmost:][:new_rightmost]
      // well, the slice syntax is RATHER like Python's d-:
      target_thumb_tag
        .append(thumb_pool.slice(new_leftmost).clone())
        .append(thumb_pool.slice(0, new_rightmost).clone());
    } else
    // scroll toward the right and wrap
    if (new_rightmost >= total_pics) {
      // new_rightmost - total_pics is the no. of imgs wrapped
      // slices: [new_leftmost:][:new_rightmost - total_pics]
      target_thumb_tag
        .append(thumb_pool.slice(new_leftmost).clone())
        .append(thumb_pool.slice(0, new_rightmost - total_pics).clone());

    } else {
      // ordinary continuous slice
      target_thumb_tag.append(thumb_pool.slice(new_leftmost, new_rightmost)
                                        .clone());
    }

    // do click event binding... everytime i refresh the list the evt handlers
    // all seem to be wiped, sigh
    // the data() solution is also not working, so we must generate the
    // sequence ourselves... to our delight it's not that difficult. Just put
    // up a counter and...
    photo_idx = new_leftmost < 0 ? total_pics + new_leftmost : new_leftmost;

    target_thumb_tag.children().each(function(i){
      // attach evt handler, we can directly invoke doGotoPhoto() here
      // because the idx is associated in advance
      //
      // Since the counter is in closure scope and thus is only retaining the
      // final value, we must consolidate the value... using closure again and
      // NO need for data(). (data() may work here though; the element isn't
      // going to change as long as we don't refresh the list...)
      // the factory function is refactored to top-closure-level; see below
      $(this).click(clickHandlerFactory(photo_idx));

      photo_idx++;
      if (photo_idx >= total_pics) // actually only == is possible...
        photo_idx -= total_pics;
    });
  }

  // just a convenient wrapper
  function alignCurrentImg()
  {
    centerAlign($(div_pres + '.photo>img'));
  }

  // update current index
  function updateIndex()
  {
    return curr_idx_tag
        ? curr_idx_tag.text((curr_idx + 1).toString())
        : undefined;
  }

  // navigation
  function doGotoPhoto(idx, initial)
  {
    // the new <img>
    // need to clone() here or the corresponding thumbnail will be gone
    var attr_visibility = 'visibility', // to help minification
        cooked_tag = image_pool.eq(idx).clone().css(attr_visibility, 'hidden'),
        old_thumb_tag = thumb_pool.eq(curr_idx), // old_idx really...
        new_thumb_tag = thumb_pool.eq(idx);

    function do_switch()
    {
      // various refreshing
      // update curr_idx
      curr_idx = idx;

      // update the index label
      updateIndex();

      // update photo title
      photo_title_tag.text(cooked_tag.attr('alt'));

      // toggle the two thumbnails' enabled attr...
      if (!initial)
        // not on initialization
        old_thumb_tag.toggleClass(cls_enabled);
      new_thumb_tag.toggleClass(cls_enabled);

      // do the real substitution
      target_photo_tag.empty().append(cooked_tag);
      // update alignment
      // must do this when layout is done
      alignCurrentImg();

      // update thumbnail list
      arrangeThumbnails(idx);

      cooked_tag
        .css(attr_visibility, 'visible')
        .hide()
        // go onward!
        .fadeIn(200);
    }

    // replace the content of div.photo!
    // for a nice fading effect...
    // FIXME: page load condition when there should be nothing inside target!!
    if (initial) {
      do_switch();
    } else {
      target_photo_tag.children().fadeOut(200, do_switch);
    }
  }

  // Generalized the way of wrapping around...
  function prevWithWrap(fn, idx)
  {
    // w/ wraparound
    return fn((idx == 0) ? total_pics - 1 : idx - 1);
  }

  function nextWithWrap(fn, idx)
  {
    // also w/ wraparound
    return fn((idx == total_pics - 1) ? 0 : idx + 1);
  }


  // event handlers, merely invoke the backend for now
  function prevPhotoClicked()
  {
    prevWithWrap(doGotoPhoto, curr_idx);
  }

  function nextPhotoClicked()
  {
    nextWithWrap(doGotoPhoto, curr_idx);
  }

  function prevThumbClicked()
  {
    prevWithWrap(arrangeThumbnails, curr_thumb_idx);
  }

  function nextThumbClicked()
  {
    nextWithWrap(arrangeThumbnails, curr_thumb_idx);
  }


  // init gallery ui
  $(document).ready(function(){
    // display the presentational tags
    $('.gal').show();
    $(div_pool).hide();

    // cache the image tag pool (is this needed to maximize performance?)
    image_pool = $(div_pool + 'img');
    // <span> for current photo index
    curr_idx_tag = $('.index>.curr');
    // (the only) div.photo tag that contains the current <img>
    target_photo_tag = $('.photo').first();
    // image title (alt prop really) in the per-photo area
    photo_title_tag = $('.perphoto .metadata>.title');

    // total numbers of images
    total_pics = image_pool.length;
    $('.index>.total').text(total_pics.toString());

    // for now, the presentation area is fixed dimension...
    // if it were to become fluid, we need to refresh UI once here

    // basic "button" events
    $(div_pres + div_prev).click(prevPhotoClicked);
    $(div_pres + div_next).click(nextPhotoClicked);

    // thumbnails
    initThumbnails();

    // initial photo
    doGotoPhoto(0, true); // initial=true
  });
})($jq17);


// vi:ai:et:ts=2:sw=2:sts=2:ff=unix:fenc=utf8:
