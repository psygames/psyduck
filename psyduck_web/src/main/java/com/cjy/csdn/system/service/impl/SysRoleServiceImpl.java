package com.cjy.csdn.system.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.entity.SysRole;
import com.cjy.csdn.system.mapper.SysRoleMapper;
import com.cjy.csdn.system.service.ISysRoleService;

@Service
public class SysRoleServiceImpl implements ISysRoleService{
    @Autowired
    private SysRoleMapper roleMapper;

    public SysRole selectById(Integer id){
        return roleMapper.selectById(id);
    }
    public SysRole selectByName(String name){
        return roleMapper.selectByName(name);
    }
}