package com.cjy.csdn.system.controller;

import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.cjy.csdn.system.model.SysUser;
import com.cjy.csdn.system.service.ISysUserService;

@Controller
public class UserController {
	private Logger logger = LoggerFactory.getLogger(UserController.class);

	@Autowired
	ISysUserService iSysUserService;

	@ResponseBody
	@RequestMapping(value = "/users/add", method = RequestMethod.POST)
	public String add(SysUser sysUser) {
		SysUser s = iSysUserService.selectByName(sysUser.getName());
		if(s != null) {
			return "用户已存在";
		}
		sysUser.setId(new Random().nextInt());
		iSysUserService.insertOne(sysUser);
		SysUser s2 = iSysUserService.selectByName(sysUser.getName());
		logger.info("添加用户" + (s2 != null));
		return "注册" + ((s2 != null)) + "，你自己返回登陆页面吧";
	}
}
