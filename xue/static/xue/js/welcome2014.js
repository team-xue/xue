(function($){
  'use strict';

  // from jQuery UI
  var easeInBounce = function(p) {
    var pow2, bounce = 4;
    while (p < ((pow2 = Math.pow(2, --bounce)) - 1) / 11) {}
    return 1 / Math.pow(4, 3 - bounce) - 7.5625 * Math.pow((pow2 * 3 - 2) / 22 - p, 2);
  };

  $.easing['easeInBounce'] = easeInBounce;
  $.easing['easeOutBounce'] = function(p) {
    return 1 - easeInBounce(1 - p);
  };

  var welcomeBannerFactory = function($container, $pusher, $retractButton, $html) {
    var self = {
      init: function() {
        // 强制显示滚动条以保证 banner 收回时动画过程中滚动条不会消失
        // 收回动画结束之后将恢复初始值 (为空)
        $html.css('overflow-y', 'scroll');

        // 绑定收回按钮点击事件
        $retractButton.click(function() {
          // hard-code 时间常数为 0.1s 按钮, 0.5s 收起动作
          self.retractBanner(100, 750);
        });
      },
      retractElem: function(elem, duration, callback) {
        // easing 固定为 easeOutBounce (弹来弹去的, 纯粹是恶趣味)
        elem.animate({height: 0}, duration, 'easeOutBounce', callback);
      },
      retractBanner: function(buttonFadeDuration, bannerRetractDuration) {
        // 先隐藏按钮
        $retractButton.animate({opacity: 0}, buttonFadeDuration, function() {
          // 按钮现在已经是累赘了, 去掉
          $retractButton.css('display', 'none');

          // 收起剩下的部分
          self.retractElem($container, bannerRetractDuration, function() {
            $container.css('display', 'none');
          });
          self.retractElem($pusher, bannerRetractDuration, function() {
            $pusher.css('display', 'none');

            // 该不显示滚动条就不显示
            $html.css('overflow-y', '');
          });
        });
      }
    };

    return self;
  };

  $(document).ready(function() {
    var welcomeBanner = welcomeBannerFactory(
      $('#welcomefresh2014-container'),
      $('#welcomefresh2014-push'),
      $('#welcomefresh2014-retract'),
      $('html')
      );
    welcomeBanner.init();
  });
})($jq);


// vi:ai:et:ts=2:sw=2:sts=2:ff=unix:fenc=utf8:
