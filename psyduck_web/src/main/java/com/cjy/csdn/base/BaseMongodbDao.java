package com.cjy.csdn.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

@Component
public class BaseMongodbDao {
	@Autowired
	private MongoTemplate mongoTemplate;
	
	public MongoTemplate getMongoTemplate() {
		return this.mongoTemplate;
	}
}

