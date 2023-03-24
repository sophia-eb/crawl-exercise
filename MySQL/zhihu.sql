CREATE SCHEMA `zhihu` DEFAULT CHARACTER SET utf8 ;

DROP TABLE salt_ranking_list;

CREATE TABLE IF NOT EXISTS `salt_ranking_list` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `author` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `media_type` varchar(45) DEFAULT NULL,
  `price` varchar(45) DEFAULT NULL,
  `description` blob,
  `summary` blob,
  `url` varchar(255) NOT NULL,
  `list_type` varchar(45) NOT NULL COMMENT '热度榜，飙升榜，上新榜',
  `json_data` json NOT NULL,
  `created_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=612 DEFAULT CHARSET=utf8mb3;
