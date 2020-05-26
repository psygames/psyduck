package com.cjy.csdn.system.dao;

import java.util.List;

import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

import com.cjy.csdn.base.BaseMongodbDao;
import com.cjy.csdn.system.model.SysUserRole;

@Component
public class SysUserRoleDao extends BaseMongodbDao{
    public List<SysUserRole> listByUserId(Integer userId){
    	Query q = new Query();
    	q.addCriteria(Criteria.where("user_id").is(userId));
    	return getMongoTemplate().find(q, SysUserRole.class);
    }
}