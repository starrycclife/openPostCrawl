layui.use(['table', 'jquery'], function () {
    var $ = layui.$;
    var table = layui.table;
    var current_jobid = Cookies.get('current_jobid');
    var current_api = Cookies.get('current_api');

    table.render({
        elem: '#video-list',
        url: host + '/api/' + current_api,
        where: {
            job_id: current_jobid
        },
        page: true,
        cellMinWidth: 200,
        cols: [
            [{
                field: 'title',
                title: '视频名称',
            }, {
                fixed: 'right',
                align: 'center',
                toolbar: '#barDemo',
                width: 100
            }]
        ]
    });

    table.on('tool(video-list)', function (obj) {
        var data = obj.data;
        var layEvent = obj.event;
        var tr = obj.tr;

        if (layEvent === 'play') {
            // $('#video-player').get(0).pause();
            // $('#video-source').attr('src', host + data.path);
            // $('#video-player').get(0).load();
            // layer.open({
            //     type: 1,
            //     title: '视频预览',
            //     content: $('#video-layer'),
            //     maxWidth: 800
            // });

            window.open(host + data.path);


        }
    });
});