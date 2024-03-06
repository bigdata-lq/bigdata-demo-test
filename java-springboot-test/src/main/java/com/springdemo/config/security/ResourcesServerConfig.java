package com.springdemo.config.security;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableResourceServer;
import org.springframework.security.oauth2.config.annotation.web.configuration.ResourceServerConfigurerAdapter;

/**
 *  * @description: 资源服务器的配置
 *  * 通常为用户，也可以是应用程序，既该资源的拥有者。
 */
@Configuration
@EnableResourceServer
public class ResourcesServerConfig extends ResourceServerConfigurerAdapter {
    @Override
    public void configure(HttpSecurity http) throws Exception {
        //所有的访问都需要认证访问
        http.authorizeRequests().anyRequest().authenticated();
        //唯独user 可以访问 放行我们的资源
        http.requestMatchers().antMatchers("/demo/user/**","/demo/auth/token");
    }

}
