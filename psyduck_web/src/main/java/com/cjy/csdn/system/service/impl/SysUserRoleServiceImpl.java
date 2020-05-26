package com.cjy.csdn.system.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cjy.csdn.system.dao.SysUserRoleDao;
import com.cjy.csdn.system.model.SysUserRole;
import com.cjy.csdn.system.service.ISysUserRoleService;

@Service
public class SysUserRoleServiceImpl implements ISysUserRoleService{
    @Autowired
    private SysUserRoleDao sysUserRoleDao;

    public List<SysUserRole> listByUserId(Integer userId) {
        return sysUserRoleDao.listByUserId(userId);
    }
}