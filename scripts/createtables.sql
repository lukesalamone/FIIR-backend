CREATE TABLE USER (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `pic` varchar(100) NOT NULL,
  `phone_number` varchar(50) NOT NULL,
  `auth_token` varchar(200) NOT NULL,
  `invited_by` bigint(20) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
