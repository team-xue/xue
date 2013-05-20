(function($){
  var items_per_page = 5,
      articles_jq = null,
      paging_stage = null,
      pool_selector = '#pagination_pool';
  function pageCallback(page_idx, jq) {
    var new_content=articles_jq.slice(page_idx * items_per_page, (page_idx + 1) * items_per_page).clone();
    paging_stage.empty().append(new_content);
    return false;
  }

  function initPagination() {
    var num_entries;
    // the list of li's must be constructed after DOM ready... or have a empty list
    articles_jq = $('#pagination_pool>li');
    // the stage...
    paging_stage = $('div.paginator_container>ul.articlelist');
    num_entries = articles_jq.length;
    $('.paginator').pagination(num_entries, {
      callback: pageCallback,
      items_per_page: items_per_page,
      load_first_page: true
      });
  }

  $(document).ready(function(){
    // hide the pool and show the js-driven paginator
    var pool=$(pool_selector);

    $('.paginator_container').show();
    pool
      .hide()
      // just to be complete... remove the 'articlelist' class from the now hidden pool
      .removeClass('articlelist')
      ;

    // reverse the article's order
    /*
    pool.children().each(function(i, li) {
      pool.prepend(li);
    });
    */

    initPagination();
  });
})($jq);


// vim:ai:et:ts=2:sw=2:sts=2:ff=unix:fenc=utf-8:
