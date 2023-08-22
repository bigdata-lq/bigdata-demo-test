use test;
CREATE TABLE `user` (
                        `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
                        `name` varchar(21) DEFAULT NULL,
                        `account` varchar(21) DEFAULT NULL,
                        `nick_name` varchar(21) DEFAULT NULL,
                        `constellation` varchar(21) DEFAULT NULL,
                        `age` int(5) DEFAULT NULL,
                        `sex` tinyint(2) DEFAULT NULL,
                        `gmt_create` datetime DEFAULT NULL,
                        `gmt_modified` datetime DEFAULT NULL,
                        `deleted` tinyint(2) DEFAULT NULL,
                        `version` int(11) DEFAULT NULL,
                        PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;