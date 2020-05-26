package com.cjy.csdn.system.model;

import java.io.Serializable;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "sysRoleColl")
public class SysRole implements Serializable {
    static final long serialVersionUID = 1L;
    
    private Integer id;

    private String name;
    
}