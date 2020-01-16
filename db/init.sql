CREATE DATABASE knights;
use knights;

CREATE TABLE `favorite_colors` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `color` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO favorite_colors
  (name, color)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');



CREATE TABLE `payments` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `provider_id` int(11) NOT NULL,
  `order_number` varchar(45) NOT NULL DEFAULT '',
  `currency_id` int(11) NOT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `status_details` varchar(255) DEFAULT NULL,
  `confirmation_code` varchar(50) DEFAULT NULL,
  `hash` varchar(255) DEFAULT NULL,
  `encrypted_data` varchar(255) DEFAULT NULL,
  `signature` varchar(255) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`,`order_number`),
  KEY `order_number` (`order_number`),
  KEY `created` (`created`,`status`),
  KEY `order_number_only_idx` (`order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=59087588 DEFAULT CHARSET=utf8;