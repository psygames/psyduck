package com.cjy.csdn.system.security;

import javax.servlet.http.HttpServletRequest;
import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationDetailsSource;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.builders.WebSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.security.core.session.SessionRegistryImpl;
import org.springframework.security.web.access.expression.DefaultWebSecurityExpressionHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.authentication.WebAuthenticationDetails;
import org.springframework.security.web.authentication.rememberme.JdbcTokenRepositoryImpl;
import org.springframework.security.web.authentication.rememberme.PersistentTokenRepository;

@Configuration
@EnableWebSecurity //(debug=true)
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private CustomUserDetailsService userDetailsService;
    
    @Autowired
    private AuthenticationDetailsSource<HttpServletRequest, WebAuthenticationDetails> customAuthenticationDetailsSource;
    
    @Autowired
    private DataSource dataSource;
    
    @Autowired
    private CustomAuthenticationProvider customAuthenticationProvider;
    
    @Autowired
    private CustomAuthenticationSuccessHandler customAuthenticationSuccessHandler;
    
    @Autowired
    private CustomAuthenticationFailureHandler customAuthenticationFailureHandler;
    
    @Autowired
    private CustomLogoutSuccessHandler logoutSuccessHandler;


     @Bean
     public PersistentTokenRepository persistentTokenRepository(){
         JdbcTokenRepositoryImpl tokenRepository = new JdbcTokenRepositoryImpl();
         tokenRepository.setDataSource(dataSource);
         // 如果token表不存在，使用下面语句可以初始化该表；若存在，请注释掉这条语句，否则会报错。
//            tokenRepository.setCreateTableOnStartup(true);
         return tokenRepository;
     }
     
     /**
      * 注入自定义PermissionEvaluator
      * 需要在properties中设置：spring.main.allow-bean-definition-overriding=true
      */
     @Bean
     public DefaultWebSecurityExpressionHandler webSecurityExpressionHandler(){
         DefaultWebSecurityExpressionHandler handler = new DefaultWebSecurityExpressionHandler();
         handler.setPermissionEvaluator(new CustomPermissionEvaluator());
         return handler;
     }
     
     @Bean
     public SessionRegistry sessionRegistry() {
         return new SessionRegistryImpl();
     }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
    	auth.authenticationProvider(customAuthenticationProvider);
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                // 如果有允许匿名的url，填在下面
//                .antMatchers().permitAll()
        		.antMatchers("/getVerifyCode","/login","/register","/users/add","/signout","/login/invalid").permitAll()
                .anyRequest().authenticated()
                // 设置登陆页
                .and().formLogin().loginPage("/login")
                // 设置登陆成功页
                .successHandler(customAuthenticationSuccessHandler)
                // 登录失败Url
                .failureHandler(customAuthenticationFailureHandler)
                
                // 设置登陆成功页
                //.defaultSuccessUrl("/").permitAll()
                // 登录失败Url
//                .failureUrl("/login/error")
                
                
                // 自定义登陆用户名和密码参数，默认为username和password
                //.usernameParameter("username")
                //.passwordParameter("password")
                //1.Spring Security方式加入验证码验证：
                //	customAuthenticationDetailsSource(登录过程中对用户的登录信息的详细信息进行填充)
                //<-CustomWebAuthenticationDetails( 获取用户登录时携带的额外信息 这里指验证码，密码和用户名在父类中默认携带)
                //<-CustomAuthenticationProvider(验证 验证码，密码)
                .authenticationDetailsSource(customAuthenticationDetailsSource)
                .and()
                //2.自定义验证码过滤器，在springsecurity执行密码验证过滤之前，先执行我们的验证码验证
                .addFilterBefore(new VerifyFilter(),UsernamePasswordAuthenticationFilter.class)
                
                //退出登录
                .logout().logoutUrl("/signout")
                .deleteCookies("JSESSIONID")
            	.logoutSuccessHandler(logoutSuccessHandler).permitAll()
                
		        // 自动登录
		        .and()
	        	//记录密码，自动登陆，cookie存在客户端
	        	.rememberMe()
	        	//登陆成功生成的token会存入数据库
		        .tokenRepository(persistentTokenRepository())
                // 有效时间：单位s
                .tokenValiditySeconds(60)
                .userDetailsService(userDetailsService)
	                
                .and()
                .sessionManagement()
                .invalidSessionUrl("/login")
                .maximumSessions(1)
            	// 当达到最大值时，是否保留已经登录的用户
            	.maxSessionsPreventsLogin(false)
            	// 当达到最大值时，旧用户被踢出后的操作
                .expiredSessionStrategy(new CustomExpiredSessionStrategy())
                .sessionRegistry(sessionRegistry());//主动踢人

        //默认都会产生一个hiden标签 里面有安全相关的验证 防止请求伪造 这边我们暂时不需要 可禁用掉
        http.csrf().disable();
    }

    @Override
    public void configure(WebSecurity web) {
        // 设置拦截忽略文件夹，可以对静态资源放行
        web.ignoring().antMatchers("/css/**", "/js/**");
    }
}
