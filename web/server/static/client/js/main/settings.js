layui.use(['jquery','form'], function () {
    var $ = layui.$;
    var form = layui.form;
    form.on('submit(form)', function (e) {
        data = e.field;
        switch (data.website) {
          case '0':
            data.website = 'weibo'
            break;
          case '1':
            data.website = 'facebook'
            break;
          case '2':
            data.website = 'twitter'
            break;
          case '3':
            data.website = 'youtube'
            break;
          default:
            break;
        }
        $.post(host + "/api/cookies", data, function (data, textStatus, jqXHR) {
          data = JSON.parse(data)
          if (data.code == 0) {
            layer.alert("Cookies修改成功", {
              icon: 1
            });
          } else {
            layer.alert(data.message, {
              icon: 2
            });
          }
        });
        return false;
      });
    
});