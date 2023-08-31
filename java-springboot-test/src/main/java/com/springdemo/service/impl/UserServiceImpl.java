package com.springdemo.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.springdemo.entity.User;
import com.springdemo.mapper.UserMapper;
import com.springdemo.service.UserService;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.io.Serializable;
import java.util.Collection;

@Service("userService")
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

//    @Resource
//    private RedisCacheManager redisCacheManager;

    @Override
//    @Cacheable(cacheNames = "user_cache", key = "'userId'+#id",unless = "#result == null",cacheManager = "redisCacheManager")
    public User getById(Serializable id) {
        //写入ehcache缓存
        //写入redis
//        Collection<String> cacheNames = redisCacheManager.getCacheNames();
//        cacheNames.forEach(name -> System.out.println("name = " + name));
//        Cache cache = redisCacheManager.getCache("redis_user_cache");
//        Cache.ValueWrapper valueWrapper = cache.get("userId-" + id);
//        if (valueWrapper != null && valueWrapper instanceof User) {
//            return (User)valueWrapper.get() ;
//        }
        User user = super.getById(id);
        //存入缓存
//        cache.put("userId-" + id, user);
        return user;
    }
}
