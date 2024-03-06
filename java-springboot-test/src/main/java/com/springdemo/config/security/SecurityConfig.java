package com.springdemo.config.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {


    /**
     * OAuth2AuthenticationManager 来处理我们密码模式的密码
     * @return
     * @throws Exception
     */
    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    /**
     * 自定义加密逻辑
     *
     * @return org.springframework.security.crypto.password.PasswordEncoder
     * @author wanglufei
     * @date 2022/4/11 6:32 PM
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }


    @Override
    protected void configure(HttpSecurity http) throws Exception {
        //关闭CSRF防护 csrf认为除了get以外的请求都是不安全的，禁用
        http.csrf().disable()
                // 授权
                .authorizeRequests()
                // 方行的请求
                .antMatchers("/demo/oauth/**", "/demo/login/**", "/demo/logout/**","/demo/user/**")
                .permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin()
                .permitAll();

    }
}
