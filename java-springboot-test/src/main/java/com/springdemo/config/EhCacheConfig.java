package com.springdemo.config;
import com.springdemo.entity.configuration.EhcacheConfiguration;
import org.ehcache.Cache;
import org.ehcache.CacheManager;
import org.ehcache.config.CacheConfiguration;
import org.ehcache.config.builders.CacheConfigurationBuilder;
import org.ehcache.config.builders.CacheManagerBuilder;
import org.ehcache.config.builders.ExpiryPolicyBuilder;
import org.ehcache.config.builders.ResourcePoolsBuilder;
import org.ehcache.config.units.EntryUnit;
import org.ehcache.config.units.MemoryUnit;
import org.ehcache.expiry.ExpiryPolicy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
@EnableCaching
public class EhCacheConfig {

    @Autowired
    private EhcacheConfiguration ehcacheConfiguration;
    @Autowired
    private ApplicationContext context;

    @Bean(name = "ehCacheManager")
    //注意此处的CacheManager是ehcache本身的不是spring的
    //原因在于spring自动加载，默认redisCacheManager 无法做选择注入
    public CacheManager getCacheManager() {
        //资源池生成器配置持久化
        ResourcePoolsBuilder resourcePoolsBuilder = 				  ResourcePoolsBuilder.newResourcePoolsBuilder()
                // 堆内缓存大小
                .heap(ehcacheConfiguration.getHeap(), EntryUnit.ENTRIES)
                // 堆外缓存大小
                .offheap(ehcacheConfiguration.getOffheap(), MemoryUnit.MB)
                // 文件缓存大小
                .disk(ehcacheConfiguration.getDisk(), MemoryUnit.MB);
        //生成配置
        ExpiryPolicy expiryPolicy = ExpiryPolicyBuilder.noExpiration();
        CacheConfiguration config = CacheConfigurationBuilder.newCacheConfigurationBuilder(String.class, Object.class, resourcePoolsBuilder)
                //设置永不过期
                .withExpiry(expiryPolicy)
                .build();

        CacheManagerBuilder cacheManagerBuilder = CacheManagerBuilder.newCacheManagerBuilder()
                .with(CacheManagerBuilder.persistence(ehcacheConfiguration.getDiskDir()));
        return cacheManagerBuilder.build(true);
    }

    @Bean(name = "ehUserCache")
    public Cache<String, Object> getEhUserCache() {
        CacheManager cacheManager = context.getBean(CacheManager.class);
        Cache<String, Object> myCache = cacheManager.createCache("eh_user_cache",
                CacheConfigurationBuilder.newCacheConfigurationBuilder(String.class, Object.class, ResourcePoolsBuilder.heap(10)).build());
        return myCache;
    }
}
