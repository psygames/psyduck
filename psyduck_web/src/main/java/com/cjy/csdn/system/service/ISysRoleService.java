package com.cjy.csdn.system.service;

import com.cjy.csdn.system.model.SysRole;

public interface ISysRoleService {

    public SysRole selectById(Integer id);
    public SysRole selectByName(String name);
}