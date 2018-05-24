var render;
var current_type = '';

layui.use(['element', 'table', 'jquery', 'layer', 'form'], function () {
  var table = layui.table;
  var $ = layui.$;
  var element = layui.element;
  var layer = layui.layer;
  var form = layui.form;
  var tableObj;

  render = function () {
    current_type = $('dd.layui-this', window.parent.document).data("id")
    title = $('dd.layui-this', window.parent.document).text()
    $('#title').text(title)
    var col1 = [{
      field: '_id',
      title: 'ID',
      width: 120,
      sort: true,
      fixed: 'left'
    }, {
      field: 'website',
      title: '网站',
      width: 120,
      sort: true
    }]
    var col2;
    if (!current_type) {
      col2 = [{
        field: 'keyword',
        title: '关键词',
        width: 120
      }, {
        field: '用户层级',
        title: 'M',
        width: 80
      }, {
        field: '用户数目',
        title: 'N',
        width: 80
      }, {
        field: 'db',
        title: '数据库',
        width: 120
      }]
      show('index_url', false);
      show('keyword', true);
      show('M', true);
      show('N', true);
      $("#website-select").empty();
      $("#website-select").append('<option value="0">微博</option>');
      $("#website-select").append('<option value="1">Facebook</option>');
      $("#website-select").append('<option value="2">Twitter</option>');
      form.render('select');
    } else {
      col2 = [{
        field: 'index_url',
        title: '主页地址',
        width: 400
      }]

      show('index_url', true);
      show('keyword', false);
      show('M', false);
      show('N', false);
      $("#website-select").empty();
      $("#website-select").append('<option value="3">YoutTube</option>');
      form.render('select');
    }
    var col3 = [{
      field: 'status',
      title: '状态',
      width: 150
    }, {
      field: 'pid',
      title: 'PID',
      width: 80
    }, {
      field: 'create_timestamp',
      title: '创建时间',
      width: 180,
      templet: function (d) {
        return new Date(d.create_timestamp * 1000).toLocaleString()
      },
      sort: true
    }, {
      fixed: 'right',
      width: 150,
      align: 'center',
      toolbar: '#barDemo'
    }]
    var options = {
      elem: '#job-list',
      url: host + '/api/jobs',
      where: {
        website: current_type
      },
      page: true,
      cols: [col1.concat(col2, col3)]
    }

    if (tableObj)
      tableObj.reload(options);
    else
      tableObj = table.render(options);


  };

  render();



  table.on('tool(job-list)', function (obj) {
    var data = obj.data;
    var layEvent = obj.event;
    var tr = obj.tr;

    if (layEvent === 'log') {
      index = layer.load(1)
      try {
        $.get(host + "/api/static?file=" + data.log, function (data, textStatus, jqXHR) {
          layer.close(index);
          data = JSON.parse(data)
          if (data.code == 0) {
            logStr = data.data[0].replace(/\n/g, "<br />");
            $('#log-layer').html(logStr)
            layer.open({
              type: 1,
              title: '日志',
              content: $('#log-layer'),
              maxWidth: 800
            });

          } else {
            layer.alert(data.message, {
              icon: 2
            });
          }
        });
      } catch (err) {
        layer.close(index);
        layer.alert(err, {
          icon: 2
        });
      }

    } else if (layEvent === 'detail') {
      Cookies.set('current_jobid', data._id);
      if (!current_type) {
        Cookies.set('current_api', 'tweet-search');
      } else {
        Cookies.set('current_api', 'youtube-videos');
      }
      window.parent.location.href = "../job-detail/";
    } else if (layEvent === 'del') {
      layer.confirm('是否确认删除此任务', function (index) {
        $.ajax({
          url: host + '/api/jobs?job_id=' + data._id,
          type: "delete",
          success: function (data, textStatus, jqXHR) {
            data = JSON.parse(data)
            if (data.code == 0) {
              layer.msg('删除成功');
              tableObj.reload();

            } else {
              layer.alert(data.message, {
                icon: 2
              });
            }
            layer.close(index);
          },
          error: function (xhr, textstatus, thrown) {
            layer.alert(textstatus, {
              icon: 2
            });
            layer.close(index);
          }
        });
      });
    }
  });
  var layerIndex;
  $("#create-job").click(function () {
    layerIndex = layer.open({
      type: 1,
      title: '创建任务',
      content: $("#create-job-layer"),
      maxWidth: 500
    });
  });
  $("#reload").click(function () {
    tableObj.reload();
  });

  form.on('submit(form)', function (e) {
    layer.close(layerIndex);
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
    $.post(host + "/api/jobs", data, function (data, textStatus, jqXHR) {
      data = JSON.parse(data)
      if (data.code == 0) {
        layer.alert("任务创建成功，PID：" + data.data[0].pid, {
          icon: 1
        });
        tableObj.reload();
      } else {
        layer.alert(data.message, {
          icon: 2
        });
      }
    });
    return false;
  });

  function show(id, show) {
    if (show) {
      $('#' + id).show();
    } else {
      $('#' + id).hide();
    }
  }

  form.verify({
    M: function (value, item) { //value：表单的值、item：表单的DOM对象
        if (!current_type) {
          if (!parseInt(value) > 0)
            return 'M值必须大于0';
        }
      }

      //我们既支持上述函数式的方式，也支持下述数组的形式
      //数组的两个值分别代表：[正则匹配、匹配不符时的提示文字]
      ,
    N: function (value, item) {
      if (!current_type) {
        if (!(1 >= parseInt(value) && parseInt(value) <= 1000))
          return 'N值的范围为1~1000';
      }
    }
  });

});