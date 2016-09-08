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



CREATE TABLE FRIENDS (
  `user_id` bigint(20) NOT NULL,
  `friend_id` bigint(20) NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`user_id`,`friend_id`),
  UNIQUE KEY `id` (`user_id`,`friend_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;









CREATE TABLE PICS (
  `user_id` bigint(20) NOT NULL,
  `date_added` datetime NOT NULL,
  `twitter_URL` varchar(200) NOT NULL,
  `instagram_URL` varchar(200) NOT NULL,
  `gps` varchar(200) NOT NULL,
  `price` bigint(20) NOT NULL,
  `filename` varchar(200) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
