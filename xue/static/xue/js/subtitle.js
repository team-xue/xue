(function($){
  var
    list_selector = ".list_vert>li>a",
    OPEN_QUOTE = /[“「]/,
    CLOSE_QUOTE = /[”」]/;

  $(document).ready(function(){
    $(list_selector).each(function(idx){
      var
        elem = $(this),
        caption = elem.text(),
        re = /—{2,}/g,
        subtitle_arr,
        last_idx = 0,
        quote_depth = 0;

      // console.log(caption);
      subtitle_arr = re.exec(caption);

      while(subtitle_arr) {
        // console.log(subtitle_arr);
        // console.log(re.lastIndex);

        // 检查是否处于引号包围之中
        // 扫描到破折号开始为止的子串
        var idx = subtitle_arr.index;
        for (i=last_idx;i<idx;i++) {
          var ch = caption.charAt(i);
          if (ch.match(OPEN_QUOTE)) {
            quote_depth++;
          } else if (ch.match(CLOSE_QUOTE)) {
            quote_depth--;
          }
        }

        last_idx = re.lastIndex;

        // 引号全部闭合？
        if (quote_depth == 0) {
          // 没有未闭合的引号了，准备在这里截断标题
          break;
        }

        // 寻找下一个破折号
        subtitle_arr = re.exec(caption);
      }

      // console.log(subtitle_arr);

      // 截断小标题
      if (subtitle_arr) {
        var
          maintitle = caption.substring(0, subtitle_arr.index).trim(),
          subtitle = caption.substring(last_idx).trim();
        // console.log(main_title);
        // console.log(subtitle);

        elem
          // 加样式标记
          .addClass("has-subtitle")
          // 替换掉原来的链接文本（长标题）
          .text(maintitle)
          // 在后边加上详细信息
          .append(
              $("<span />")
                .append($("<span />").text(maintitle).addClass("maintitle"))
                .append($("<span />").text(subtitle).addClass("subtitle"))
                .addClass("subtitlebox")
              );
      }
    });
  });
})($jq);


// vim:set ai et ts=2 sw=2 sts=2 fenc=utf-8:
