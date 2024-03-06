package com.springdemo.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.springdemo.entity.User;
import com.springdemo.hander.limit.AccessLimit;
import com.springdemo.service.UserService;
import org.apache.ibatis.annotations.Delete;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.Arrays;
import java.util.Collection;
import java.util.Map;

@RestController
@RequestMapping("user")
public class UserController {

    @Autowired
    @Qualifier("redisCacheManager")
    private CacheManager redisCacheManager;

    @Autowired
    @Qualifier("ehUserCache")
    private org.ehcache.Cache<String, Object> ehUserCache;
    /**
     * 服务对象
     */
    @Resource
    private UserService userService;


    @RequestMapping("/getCurrentUser")
    //authentication 认证
    public Object getCurrentUser(Authentication authentication) {
        return authentication.getPrincipal();
    }


    @GetMapping("cacheTest/{id}")
    public ResponseEntity cacheTest(@PathVariable("id") Integer id) {
        //先从redis中取
        Collection<String> cacheNames = redisCacheManager.getCacheNames();
        cacheNames.forEach(name -> System.out.println("name = " + name));

        Cache cache = redisCacheManager.getCache("redis_user_cache");
        Cache.ValueWrapper valueWrapper = cache.get("userId-" + id);
        if (valueWrapper != null && valueWrapper.get() != null) {
            return ResponseEntity.ok().body((User)valueWrapper.get()) ;
        }

        // 从二级缓存中取
        if(ehUserCache.get("userId-" + id) != null){
            return ResponseEntity.ok().body((User)ehUserCache.get("userId-" + id)) ;
        }

        // 数据库查
        User user = userService.getById(id);
        // 缓存双写
        cache.put("userId-" + id, user);
        ehUserCache.put("userId-" + id, user);

        return ResponseEntity.ok().body(user);
    }

    /**
     * 通过主键查询单条数据
     *
     * @param id 主键
     * @return 单条数据
     */
    @GetMapping("{id}")
    @AccessLimit
    public ResponseEntity selectOne(@PathVariable("id") Integer id) {
        return ResponseEntity.ok().body(userService.getById(id));
    }

    /**
     * 通过reqMap查询 数据
     *
     * @param reqMap 主键
     * @return 数据
     */
    @PostMapping("/list/map")
    public ResponseEntity selectByMap(@RequestBody Map<String, Object> reqMap) {
        Collection<User> users = userService.listByMap(reqMap);
        return ResponseEntity.ok().body(users);
    }

    /**
     * 列表数据
     *
     * @return 列表数据
     */
    @GetMapping
    public ResponseEntity list(User user,
                               @RequestParam(name = "pageNo", defaultValue = "1") Integer pageNo,
                               @RequestParam(name = "pageSize", defaultValue = "10") Integer pageSize) {
        Page<User> page = new Page<>(pageNo, pageSize);
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        wrapper.setEntity(user);
        IPage<User> pageList = userService.page(page, wrapper);
        return ResponseEntity.ok().body(pageList);
    }

    /**
     * 列表数据
     *
     * @return 列表数据
     */
    @GetMapping("list")
    public ResponseEntity list() {
        return ResponseEntity.ok().body(userService.list());
    }

    /**
     * 修改数据
     *
     * @param user 实例对象
     * @return 实例对象
     */
    @PostMapping
    public ResponseEntity save(@Validated User user) {
        boolean save = userService.saveBatch(Arrays.asList(user));
        return ResponseEntity.ok().body(save);
    }

    /**
     * 新增或修改数据
     *
     * @param user 实例对象
     * @return 实例对象
     */
    @PutMapping
    public ResponseEntity saveOrUpdate(User user) {
        return ResponseEntity.ok().body(userService.saveOrUpdate(user));
    }

    /**
     * 修改数据
     *
     * @param user 实例对象
     * @return 实例对象
     */
    @PutMapping("updateById")
    public ResponseEntity updateById(User user) {
        boolean b = userService.updateById(user);
        return ResponseEntity.ok().body(b);
    }

    /**
     * 通过主键删除数据
     *
     * @param id 主键
     * @return 是否成功
     */
    @Delete("{id}")
    public ResponseEntity delete(@PathVariable("id") Integer id) {
        return ResponseEntity.ok().body(userService.removeById(id));
    }

}
