package com.cjy.csdn.system.service.impl;


import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.entity.SysPermission;
import com.cjy.csdn.system.mapper.SysPermissionMapper;
import com.cjy.csdn.system.service.ISysPermissionService;

@Service
public class SysPermissionServiceImpl implements ISysPermissionService{
    @Autowired
    private SysPermissionMapper permissionMapper;

    /**
     * 获取指定角色所有权限
     */
    public List<SysPermission> listByRoleId(Integer roleId) {
        return permissionMapper.listByRoleId(roleId);
    }
}

