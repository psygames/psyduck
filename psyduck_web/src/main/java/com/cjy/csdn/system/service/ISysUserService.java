package com.cjy.csdn.system.service;

import com.cjy.csdn.system.model.SysUser;

public interface ISysUserService {

    public SysUser selectById(Integer id) ;

    public SysUser selectByName(String name) ;
    
    public void insertOne(SysUser u) ;
}