package com.springdemo.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import javax.validation.constraints.Max;
import javax.validation.constraints.NotNull;
import java.io.Serializable;
import java.util.Collection;
import java.util.Date;
import java.util.List;

@Data
public class User implements UserDetails,Serializable {

    private static final long serialVersionUID = 331645245830355567L;

    @TableId(type = IdType.AUTO)
    private Long id;
    /**
     * 用户名称
     */
    @NotNull(message = "用户名不能为空")
    private String name;
    /**
     * 账号
     */
    private String account;
    /**
     * 外号-诨名
     */
    @NotNull(message = "外号-诨名不能为空")
    private String nickName;
    /**
     * 星宿
     */
    private String constellation;
    /**
     * 年龄
     */
    @Max(value = 99, message = "不能大于200岁")
    private Integer age;
    /**
     * 性别
     */
    private Integer sex;
    /**
     * 创建时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    // 字段添加填充内容
    @TableField(fill = FieldFill.INSERT)
    private Date gmtCreate;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date gmtModified;

    /**
     * 逻辑删除
     */
    @TableLogic
    private Integer deleted;

    /**
     * 乐观锁 #OptimisticLockerInnerInterceptor
     * 当要更新一条记录的时候，希望这条记录没有被别人更新
     * 乐观锁实现方式：
     *  取出记录时，获取当前version
     *  更新时，带上这个version
     *  执行更新时， set version = newVersion where version = oldVersion
     *  如果version不对，就更新失败
     */
    @Version
    private Integer version;

    /**
     * 密码
     */
    private String password;

    /**
     * 授权
     */
    private List<GrantedAuthority> authorities;

    public User() {
    }

    public User(String name, String password, List<GrantedAuthority> authorities) {
        this.name = name;
        this.password = password;
        this.authorities = authorities;
    }

    @Override
    public String getUsername() {
        return name;
    }

    @Override
    public String getPassword() {
        return password;
    }


    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }


    @Override
    public boolean isEnabled() {
        return false;
    }
}
