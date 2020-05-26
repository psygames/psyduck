package com.cjy.csdn.system.service.impl;


import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.dao.SysPermissionDao;
import com.cjy.csdn.system.model.SysPermission;
import com.cjy.csdn.system.service.ISysPermissionService;

@Service
public class SysPermissionServiceImpl implements ISysPermissionService{
    @Autowired
    private SysPermissionDao sysPermissionDao;

    /**
     * 获取指定角色所有权限
     */
    public List<SysPermission> listByRoleId(Integer roleId) {
        return sysPermissionDao.listByRoleId(roleId);
    }
}

