package com.cjy.csdn.system.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.dao.SysUserDao;
import com.cjy.csdn.system.model.SysUser;
import com.cjy.csdn.system.service.ISysUserService;

@Service
public class SysUserServiceImpl implements ISysUserService{
    @Autowired
    private SysUserDao sysUserDao;

    public SysUser selectById(Integer id) {
        return sysUserDao.selectById(id);
    }

    public SysUser selectByName(String name) {
        return sysUserDao.selectByName(name);
    }
    
    public void insertOne(SysUser u) {
    	sysUserDao.insertOne(u);
    }
}