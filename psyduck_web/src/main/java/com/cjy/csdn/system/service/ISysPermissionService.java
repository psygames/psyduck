package com.cjy.csdn.system.service;


import java.util.List;

import com.cjy.csdn.system.model.SysPermission;

public interface ISysPermissionService {
    /**
     * 获取指定角色所有权限
     */
    public List<SysPermission> listByRoleId(Integer roleId);
}

