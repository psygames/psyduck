package com.cjy.csdn.system.controller;

import java.io.IOException;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.session.SessionInformation;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@Controller
public class LoginController {
	private Logger logger = LoggerFactory.getLogger(LoginController.class);

	@Autowired
	private SessionRegistry sessionRegistry;

	@RequestMapping(value = "/login", method = RequestMethod.GET)
	public String showLogin() {
		logger.info("跳转到登陆页面");
		return  "login";
	}
	
	@RequestMapping(value="/register", method = RequestMethod.GET)
	public String  index() {
		logger.info("跳转到注册页面");
		return "register";
	}

	@RequestMapping("/login/invalid")
	@ResponseStatus(HttpStatus.UNAUTHORIZED)
	@ResponseBody
	public String invalid() {
		logger.info("Session 已过期，请重新登录");
		return "Session 已过期，请重新登录";
	}
	
	@RequestMapping("/login/error")
	public void loginError(HttpServletRequest request, HttpServletResponse response) {
		response.setContentType("text/html;charset=utf-8");
		AuthenticationException exception = (AuthenticationException) request.getSession()
				.getAttribute("SPRING_SECURITY_LAST_EXCEPTION");
		try {
			response.getWriter().write(exception.toString());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@RequestMapping("/kick")
	@ResponseBody
	public String removeUserSessionByUsername() {
		int count = 0;
		String userName;
		String name = SecurityContextHolder.getContext().getAuthentication().getName();
		if ("admin".equalsIgnoreCase(name)) {
			userName = "jitwxs";
		} else {
			userName = "admin";
		}
		logger.info("当前登录用户：" + name + ",要踢出的用户：" + userName);

		// 获取session中所有的用户信息
		List<Object> users = sessionRegistry.getAllPrincipals();
		for (Object principal : users) {
			if (principal instanceof User) {
				String principalName = ((User) principal).getUsername();
				if (principalName.equals(userName)) {
					// 参数二：是否包含过期的Session
					List<SessionInformation> sessionsInfo = sessionRegistry.getAllSessions(principal, false);
					if (null != sessionsInfo && sessionsInfo.size() > 0) {
						for (SessionInformation sessionInformation : sessionsInfo) {
							sessionInformation.expireNow();
							count++;
						}
					}
				}
			}
		}
		String msg = "操作成功，清理session共" + count + "个";
		logger.info(msg);
		return msg;
	}
}
