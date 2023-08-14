package com.demo.options

case class RedisSinkProperty(
                              val host: String,
                              val port: Int,
                              val password: String,
                              val prefix: String,
                              val dataType: String,
                              val expireTime: Int,
                              val database: Int,
                              val ignoreDelete: Boolean
                            ) {

}
