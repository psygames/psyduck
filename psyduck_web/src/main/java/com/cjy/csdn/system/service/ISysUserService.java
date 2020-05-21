package com.cjy.csdn.system.service;

import com.cjy.csdn.system.entity.SysUser;

public interface ISysUserService {

    public SysUser selectById(Integer id) ;

    public SysUser selectByName(String name) ;
    
    public void insertOne(SysUser u) ;
}