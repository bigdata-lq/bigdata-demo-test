package com.springdemo.config.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.config.annotation.configurers.ClientDetailsServiceConfigurer;
import org.springframework.security.oauth2.config.annotation.web.configuration.AuthorizationServerConfigurerAdapter;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableAuthorizationServer;
import org.springframework.security.oauth2.config.annotation.web.configurers.AuthorizationServerEndpointsConfigurer;
import org.springframework.security.oauth2.config.annotation.web.configurers.AuthorizationServerSecurityConfigurer;
import org.springframework.security.oauth2.provider.token.TokenStore;

@Configuration
@EnableAuthorizationServer
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private PasswordEncoder passwordEncoder;
    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserDetailsService userDetailsService;

    @Autowired
    @Qualifier("redisTokenStore")
    private TokenStore redisTokenStore;





    /**
     * 密码模式是直接将我们的密码传给授权服务器
     * 使用密码所需要的配置
     *
     * @param endpoints
     * @author wanglufei
     * @date 2022/4/11 10:41 PM
     */
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints.authenticationManager(authenticationManager)
                .userDetailsService(userDetailsService)
                //配置使用redis存储token 令牌
                .tokenStore(redisTokenStore);
    }

//    /**
//     * 认证服务器的安全配置
//     *
//     * @param security
//     * @throws Exception
//     */
//    @Override
//    public void configure(AuthorizationServerSecurityConfigurer security) throws Exception {
//        security
//                //.realm(RESOURCE_ID)
//                // 开启/oauth/token_key验证端口认证权限访问
//                .tokenKeyAccess("isAuthenticated()")
//                //  开启/oauth/check_token验证端口认证权限访问
//                .checkTokenAccess("isAuthenticated()")
//                //允许表单认证
//                .allowFormAuthenticationForClients();
//    }


    /**
     * 授权服务器的4个端点
     * * - `Authorize Endpoint` ：授权端点，进行授权
     * * - `Token Endpoint` ：令牌端点，进过授权拿到对应的Token
     * * - `Introspection Endpoint`：校验端点，校验Token的合法性
     * * - `Revocat ion Endpoint` ：撤销端点，撒销授权
     *
     * @param clients
     * @author wanglufei
     * @date 2022/4/11 7:47 PM
     */
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
                //配置client Id
                .withClient("admin")
                //client-secret
                .secret(passwordEncoder.encode("112233"))
                //配置访问token的有效期
                .accessTokenValiditySeconds(3600)
                //配置重定向的跳转，用于授权成功之后的跳转
                .redirectUris("http://www.baidu.com")
                //作用域
                .scopes("all")
                //Grant_type  密码模式
                .authorizedGrantTypes("password");
    }


}
