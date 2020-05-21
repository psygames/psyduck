package com.cjy.csdn.system.service;

import java.util.List;

import com.cjy.csdn.system.entity.SysUserRole;

public interface ISysUserRoleService {

    public List<SysUserRole> listByUserId(Integer userId);
}