package com.cjy.csdn.system.dao;


import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

import com.cjy.csdn.base.BaseMongodbDao;
import com.cjy.csdn.system.model.SysUser;

@Component
public class SysUserDao extends BaseMongodbDao{
    public SysUser selectById(Integer id) {
    	return getMongoTemplate().findById(id, SysUser.class);
    }

    public SysUser selectByName(String name) {
    	Query q = new Query();
    	q.addCriteria(Criteria.where("name").is(name));
    	return getMongoTemplate().findOne(q, SysUser.class);
    }
    
    public void insertOne(SysUser u) {
    	getMongoTemplate().save(u);
    }
}