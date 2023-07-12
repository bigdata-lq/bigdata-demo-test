
-- nginx日志采集脚本
local cjson = require "cjson"
local producer = require "resty.kafka.producer"
local broker_list = {
	{ host = "192.168.115.28", port = 9092 },
	{ host = "192.168.115.29", port = 9092 },
	{ host = "192.168.115.30", port = 9092 }
}
local request_method = ngx.var.request_method
local uri = ngx.var.uri
ngx.req.read_body()
-- 定义kafka异步生产者
local bp = producer:new(broker_list, { producer_type = "sync", required_acks = -1 })
-- 发送日志消息,send第二个参数key,用于kafka路由控制:
-- key为nill(空)时，一段时间向同一partition写入数据
-- 指定key，按照key的hash写入到对应的partition

if "/bigdata/app/url" == uri and "POST" == request_method then
    --转换字符串为json对象
	local ok, err = bp:send("app-url-test2", nil, ngx.req.get_body_data())
   if not ok then
        ngx.log(ngx.ERR, "kafka send app-url topic err:", err)
        ngx.say('{"code":500}')
   elseif ok then
        ngx.say('{"code":200}')
   end
elseif "/bigdata/app/button" == uri and "POST" == request_method then
    -- ngx.log(ngx.ERR, "类型------", type(ngx.req.get_body_data()))
    local messages = cjson.decode(ngx.req.get_body_data())
    for k, v in pairs(messages["data"]) do
        local ok, err = bp:send("app-button-test2", nil, cjson.encode(v))
        if not ok then
            ngx.log(ngx.ERR, "kafka send app-button topic err:", err)
            return
        end
    end
    ngx.say('{"code":200}')
else
	ngx.say('{"code":500}')
end