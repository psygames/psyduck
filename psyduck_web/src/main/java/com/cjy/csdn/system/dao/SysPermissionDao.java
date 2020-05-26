package com.cjy.csdn.system.dao;

import java.util.List;

import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

import com.cjy.csdn.base.BaseMongodbDao;
import com.cjy.csdn.system.model.SysPermission;

@Component
public class SysPermissionDao extends BaseMongodbDao{
	
    public List<SysPermission> listByRoleId(Integer roleId){
    	Query query=new Query(Criteria.where("role_id").is(roleId));
    	List<SysPermission> list = getMongoTemplate().find(query, SysPermission.class);
    	return list;
    }
    
}

