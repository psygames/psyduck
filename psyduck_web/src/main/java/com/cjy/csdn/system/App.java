package com.cjy.csdn.system;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.session.data.redis.config.annotation.web.http.EnableRedisHttpSession;

import com.cjy.csdn.system.security.VerifyServlet;

@EnableRedisHttpSession
@SpringBootApplication
public class App 
{
    public static void main( String[] args )
    {
    	SpringApplication.run(App.class,args);
    }
    
    /**
     * 注入验证码servlet
     */
    @Bean
    public ServletRegistrationBean<VerifyServlet> indexServletRegistration() {
        ServletRegistrationBean<VerifyServlet> registration = new ServletRegistrationBean<VerifyServlet>(new VerifyServlet());
        registration.addUrlMappings("/getVerifyCode");
        return registration;
    }
}
