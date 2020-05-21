package com.cjy.csdn.system.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.entity.SysUser;
import com.cjy.csdn.system.mapper.SysUserMapper;
import com.cjy.csdn.system.service.ISysUserService;

@Service
public class SysUserServiceImpl implements ISysUserService{
    @Autowired
    private SysUserMapper userMapper;

    public SysUser selectById(Integer id) {
        return userMapper.selectById(id);
    }

    public SysUser selectByName(String name) {
        return userMapper.selectByName(name);
    }
    
    public void insertOne(SysUser u) {
    	userMapper.insertOne(u);
    }
}