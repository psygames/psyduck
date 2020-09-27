var murmur = '';
var current_page = 0;
var result_json = '';
var bottom_loading = false;
var search_done = false;

function catch_murmur()
{
    setTimeout(function ()
    {
        Fingerprint2.get(function (components)
        {
            var values = components.map(function (component) { return component.value })
            murmur = Fingerprint2.x64hash128(values.join(''), 31)
        })
    }, 500)
}

setTimeout("catch_murmur()", 50);

function onKeyDown(event)
{
     var e = event || window.event || arguments.callee.caller.arguments[0];
     if(e && e.keyCode==13)// enter 键
     {
        search();
     }
}

function search()
{
    clear();
    search_continue();
	bottom_load();
}

function search_continue()
{
    var keyword = $("#keyword").val();
	if(search_done)
		return;
    var cip = returnCitySN["cip"];
    var cname = returnCitySN["cname"]
    $.ajax({
        type: 'POST',
        url: 'search',
        data: {'murmur': murmur, 'keyword': keyword, 'page': current_page, 'cip': cip, 'cname': cname},
        dataType: 'json',
        success: function(res) {
            bottom_load_end();
            append_result(res.result_json)
        },
        error: function() {
            console.log('请求失败~');
        }
    });
}

function clear()
{
	search_done = false;
    current_page = 0;
	bottom_load_end();
    $("#p").html('');
}

function append_result(result_json)
{
    var _result = JSON.parse(result_json)["result"];
    var _rank = 1 + current_page * 10;
    var _html = "";
	if(_result.length < 10)
		search_done = true;
    for(var index in _result)
    {
        var item = _result[index]["info"];
        var share_url = _result[index]["share_url"]
        var url = item['url'];
        var _star = item["star"];
        var _desc = item["description"];
        var _title = item["title"];
        var _date = item["upload_time"];

        var dl = '<dl class="form-inline form-group">';
        dl += '<dt><a href="'+ share_url +'" target="_blank" style="font-size:18px"><b>';
        dl += _rank + '. '+ _title +'</b></a></dt>';
        dl += '<dd><p class="text-muted">* '+_desc+'</p><p class="text-muted">时间：'+_date+'　　评分：<span style="font-size:20px;height:16px;">'+_star+'</span></p></dd>';
        dl += '</dl>';
        dl += '<hr>';
        _html += dl;
        _rank += 1;
    }

    $("#p").append(_html);
}

function bottom_load()
{
    bottom_loading = true;
    $("#bottom_load").html('加载数据中...');
}

function bottom_load_end()
{
    bottom_loading = false;
    $("#bottom_load").html('');
}

function search_done_html()
{
    $("#bottom_load").html('没有更多数据了');
}

$(window).scroll(function(){
　　var scrollTop = $(this).scrollTop();
　　var scrollHeight = $(document).height();
　　var windowHeight = $(this).height();
　　if(scrollTop + windowHeight == scrollHeight)
    {
		if(bottom_loading)
			return;
		if(search_done)
		{
			search_done_html();
			return;
		}
			
        current_page += 1;
        bottom_load();
        search_continue();
　　}
});