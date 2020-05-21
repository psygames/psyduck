package com.cjy.csdn.system.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.entity.SysUserRole;
import com.cjy.csdn.system.mapper.SysUserRoleMapper;
import com.cjy.csdn.system.service.ISysUserRoleService;

@Service
public class SysUserRoleServiceImpl implements ISysUserRoleService{
    @Autowired
    private SysUserRoleMapper userRoleMapper;

    public List<SysUserRole> listByUserId(Integer userId) {
        return userRoleMapper.listByUserId(userId);
    }
}