layui.use(['element', 'table', 'jquery', 'layer', 'form'], function () {
  var table = layui.table;
  var $ = layui.$;
  var element = layui.element;
  var layer = layui.layer;

  var tableObj = table.render({
    elem: '#job-list',
    url: host + '/jobs',
    page: true,
    cols: [
      [{
        field: '_id',
        title: 'ID',
        width: 120,
        sort: true,
        fixed: 'left'
      }, {
        field: 'keyword',
        title: '关键词',
        width: 120
      }, {
        field: 'website',
        title: '网站',
        width: 120,
        sort: true
      }, {
        field: 'M',
        title: 'M',
        width: 80
      }, {
        field: 'N',
        title: 'N',
        width: 80
      }, {
        field: 'db',
        title: '数据库',
        width: 120
      }, {
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
    ]
  });

  table.on('tool(job-list)', function (obj) {
    var data = obj.data;
    var layEvent = obj.event;
    var tr = obj.tr;

    if (layEvent === 'log') {
      index = layer.load(1)
      try {
        $.get(host + "/static?file=" + data.log, function (data, textStatus, jqXHR) {
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
      Cookies.set('current_api', 'tweet-search');
      window.parent.location.href="../job-detail/"; 
    } else if (layEvent === 'del') {
      layer.confirm('真的删除行么', function (index) {
        obj.del();
        layer.close(index);
        //向服务端发送删除指令
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

  var form = layui.form;

  //监听提交
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
    $.post(host + "/jobs", data, function (data, textStatus, jqXHR) {
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

  form.on('select(website)', function (data) {
    if (data.value) {
      if (data.value == 3) {
        show('index_url', true);
        show('keyword', false);
        show('M', false);
        show('N', false);
      } else {
        show('index_url', false);
        show('keyword', true);
        show('M', true);
        show('N', true);
      }
    } else {
      show('index_url', false);
      show('keyword', false);
      show('M', false);
      show('N', false);
    }
  })

});