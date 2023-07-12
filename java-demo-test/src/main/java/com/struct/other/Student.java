package com.struct.other;

import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@NoArgsConstructor
public class Student {


    /**
     * id : 1
     * name : 李权
     * age : 32
     * gsonformat  插件测试
     */

    private long id;
    private String name;
    private int age;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }


    public static void main(String[] args) {
        Student student = new Student();
        //  option + enter健 默认生成所有的set方法
//        student.setId(0L);
//        student.setName("");
//        student.setAge(0);

        List<String> list = new ArrayList<>();
        list.stream().map(String::length).collect(Collectors.toList());
//        Collection<String> collect = list.stream().collect(Collectors.toCollection())

//        TabNine::config
    }
}
