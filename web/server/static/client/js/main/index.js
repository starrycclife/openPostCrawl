layui.use(['jquery'], function () {
    var $ = layui.$;
    $('dd').click(function () {

        var current_type = $(this).data("id")
        if (current_type == 'settings') {
            $('.container').attr("src", "./main/settings.html")
        } else {
            if ($('.container').prop('src').indexOf('main/job-list.html') == -1) {
                $('.container').attr("src", "./main/job-list.html")
            } else
                document.getElementById("container").contentWindow.render();
        }


    })
});