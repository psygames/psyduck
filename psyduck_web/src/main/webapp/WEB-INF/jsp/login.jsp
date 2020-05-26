<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD//XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>登陆</title>
</head>
<script>
	function refresh(obj) {
		obj.src = "getVerifyCode?" + Math.random();
	}
	function mouseover(obj) {
		obj.style.cursor = "pointer";
	}
</script>
<body>
	<h1>登陆</h1>
	<form method="post" action="/login">
		<div>
			用户名：<input type="text" name="username">
		</div>
		<div>
			密密码：<input type="password" name="password">
		</div>
		<div>
			<span><input type="text" class="form-control" name="verifyCode" 
				required="required" placeholder="验证码"> 
				<img src="getVerifyCode" title="看不清，请点我" onclick="refresh(this)"
				onmouseover="mouseover(this)" />
			</span>
		</div>
		<div>
			<!--         <label><input type="checkbox" name="remember-me"/>自动登录</label> -->
			<button type="submit">立即登陆</button>
			<a href="/register">注册</a>
		</div>
	</form>
</body>
</html>
