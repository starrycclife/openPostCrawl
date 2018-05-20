layui.use(['laypage', 'jquery'], function () {
    var laypage = layui.laypage;
    var $ = layui.$;
    var current_jobid = Cookies.get('current_jobid');

    function render(current_api) {
        if (current_api)
            Cookies.set('current_api', current_api);
        else
            current_api = Cookies.get('current_api');

        $.get(host + '/api/' + current_api + '?page=' + 1 + '&limit=' + 10 + "&job_id=" + current_jobid, function (data) {
            data = JSON.parse(data)
            if (data.code == 0) {
                laypage.render({
                    elem: 'page-btn',
                    count: data.count,
                    layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
                    jump: function (obj, first) {
                        var page = obj.curr;
                        var limit = obj.limit;
                        if (!first) {
                            $.get(host + '/api/' + current_api + '?page=' + page + '&limit=' + limit + "&job_id=" + current_jobid, function (data) {
                                data = JSON.parse(data)
                                if (data.code == 0) {
                                    $("#json").JSONView(data.data);
                                } else {
                                    layer.msg(data.message);
                                }
                            });
                        }

                    }
                });

                $("#json").JSONView(data.data);
            } else {
                layer.msg(data.message);
            }
        });

    };

    render();

    $('dd', window.parent.document).click(function () {
        $('#title').text($(this).text());
        render($(this).data('api'));


    })


});