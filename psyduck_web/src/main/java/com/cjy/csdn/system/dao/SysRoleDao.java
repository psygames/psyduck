package com.cjy.csdn.system.dao;

import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

import com.cjy.csdn.base.BaseMongodbDao;
import com.cjy.csdn.system.model.SysRole;

@Component
public class SysRoleDao  extends BaseMongodbDao{
	
    public SysRole selectById(Integer id) {
    	return getMongoTemplate().findById(id, SysRole.class);
    }
	
    public SysRole selectByName( String name) {
    	Query query = new Query(Criteria.where("name").is(name));
    	return getMongoTemplate().findOne(query, SysRole.class);
    }
}