<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>注册</title>
</head>
<script type="text/javascript">
function check() { 
	var name = document.getElementById("name");
	if(name == null || name ==""){
		alert('账号不能为空');
		return;
	}
	var p1 = document.getElementById("password");
	var p2 = document.getElementById("password2");
	if(p1 != p2 &&(p1.value != p2.value)){
		alert("密码不一致");
		return;
	}
	if(p1 == null || p1 == ""){
		alert('密码不能为空');
		return;
	}
	document.getElementById("form1").submit();
}
</script>
<body>
	<form method="post" action="/users/add" id="form1">
		<div><span><label>账号:</label><input type="text" name="name" id = "name" maxlength="20"></span></div>
		<div><span><label>密码:</label><input type="password" name="password"  id = "password" maxlength="6"></span></div>
		<div><span><label>确认密码:</label><input type="password" id = "password2"></span></div>
		<div><span><input type="button" value='注册' onclick="check();" ></span></div>
	</form>
</body>
</html>