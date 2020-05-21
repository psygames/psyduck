package com.cjy.csdn.system.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import com.cjy.csdn.system.entity.SysRole;

@Mapper
public interface SysRoleMapper {
	@Select("SELECT * FROM sys_role WHERE id = #{id}")
    SysRole selectById(Integer id);
	
	@Select("SELECT * FROM sys_role WHERE name = #{name}")
    SysRole selectByName(String name);
}