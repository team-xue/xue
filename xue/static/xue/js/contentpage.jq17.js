(function($){
  // fix nested table
  $(document).ready(function(){
    $('.cms_article td>table:only-child').css('margin', 0)
    .parent().css('padding', 0);

  /*
   * TODO: split share widgets out
   */
  /*
  });
})($jq17);

(function($){
  $(document).ready(function(){
  */

    // share content
    var
      renren_like_iframe,
      weibo_share_iframe,
      shareInfo=x_shareInfo,
      pageurl=shareInfo['u'],
      pagetitle=shareInfo['t'],
      pagedesc=shareInfo['d'],
      pageimg=shareInfo['i'],
      as_encodeURIComponent=encodeURIComponent;

    renren_like_iframe = (function(){
      var
        p=[],
        w=210,
        h=65,
        lk={
          url: pageurl,
          title: pagetitle,
          description: pagedesc,
          image: pageimg
          };
    
      for(var i in lk) {
        p.push(i + '=' + as_encodeURIComponent(lk[i]||''));
      }

      return '<iframe scrolling="no" frameborder="0" allowtransparency="true" src="http://www.connect.renren.com/like/v2?'+p.join('&')+'" style="width:'+w+'px;height:'+h+'px;"></iframe>';
    })();

    weibo_share_iframe = (function(){
      var
        _w=90,
        _h=24,
        param={
          url: pageurl,
          type: '2',
          count: '1',
          appkey: '',
          title: pagetitle,
          pic: pageimg,
          ralateUid: '',
          language: 'zh_cn',
          rnd:new Date().valueOf()
          },
        temp=[];

      for(var p in param) {
        temp.push(p + '=' + as_encodeURIComponent(param[p] || ''));
      }

      return '<iframe allowTransparency="true" frameborder="0" scrolling="no" src="http://hits.sinajs.cn/A1/weiboshare.html?' + temp.join('&') + '" width="'+ _w+'" height="'+_h+'"></iframe>';
    })();

    $('#sharePlaceholder').append(
        // Renren Like
        $(renren_like_iframe)
        )
      .append(
          // Renren Share script
          (function(){
            var elem=document.createElement('script');
            
            elem.type = 'text/javascript';
            elem.async = true;
            elem.src = "http://widget.renren.com/js/rrshare.js";

            return $(elem);
          })()
          )
      .append(
          // Renren Share
          $('<a name="xn_share" type="button_medium" href="javascript:;"></a>')
          .click(function(){
            var rrShareParam={
              resourceUrl: pageurl,
              srcUrl: '',
              pic: pageimg,
              title: pagetitle,
              description: pagedesc
              };

            rrShareOnclick(rrShareParam);
          })
          )
      .append(
          // Weibo Share
          $(weibo_share_iframe)
          );
  });
})($jq17);


// vim:ai:et:ts=2:sw=2:sts=2:ff=unix:fenc=utf-8:
