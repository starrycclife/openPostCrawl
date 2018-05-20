layui.use(['jquery'], function () {
    var $ = layui.$;
    
    if(Cookies.get('current_api') == 'youtube-videos'){
        $('#tweet').hide();
        $('#video').show();
        $('.container').attr("src","./video-info.html") 
    }else{
        $('#video').hide();
        $('#tweet').show();
        $('.container').attr("src","./job-info.html") 
    }
});