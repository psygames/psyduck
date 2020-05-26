package com.cjy.csdn.system.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.dao.SysRoleDao;
import com.cjy.csdn.system.model.SysRole;
import com.cjy.csdn.system.service.ISysRoleService;

@Service
public class SysRoleServiceImpl implements ISysRoleService{
    @Autowired
    private SysRoleDao roleDao;

    public SysRole selectById(Integer id){
        return roleDao.selectById(id);
    }
    public SysRole selectByName(String name){
        return roleDao.selectByName(name);
    }
}