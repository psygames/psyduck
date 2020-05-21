<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>主页</title>
</head>
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$.ajax({
			url : "/users/accounts/list",
			success : function(result) {
				$("#div1").html(result);
			}
		});
	});
</script>
<body>
    <h1>账号信息列表</h1>
    <div id="acList"></div>
    <a href="/signout">退出</a>
</body>
</html>