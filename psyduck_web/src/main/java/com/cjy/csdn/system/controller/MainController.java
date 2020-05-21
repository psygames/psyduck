package com.cjy.csdn.system.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class MainController {
	private Logger logger = LoggerFactory.getLogger(MainController.class);

	@RequestMapping(value = "/main", method = RequestMethod.GET)
	public String index() {
		String name = SecurityContextHolder.getContext().getAuthentication().getName();
		logger.info("当前登陆用户：" + name);
		return "main";
	}
	
	@RequestMapping(value = "/main/admin", method = RequestMethod.GET)
	@ResponseBody
	@PreAuthorize("hasPermission('/admin','c') and hasPermission('/admin','r')")
	public String printAdmin() {
		return "如果你看见这句话，说明你访问/admin路径具有crud权限";
	}

	@RequestMapping(value = "/main/admin/c", method = RequestMethod.GET)
	@ResponseBody
	@PreAuthorize("hasPermission('/admin','c')")
	public String printAdminC() {
		return "如果你看见这句话，说明你访问/admin路径具有c权限";
	}

}
