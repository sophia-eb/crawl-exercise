DROP TABLE user_details;

CREATE TABLE IF NOT EXISTS `user_details` (
   `id` INT UNSIGNED AUTO_INCREMENT,
   `user_id` BIGINT NOT NULL,
   `user_name` CHAR(255) NOT NULL,
   `gender` CHAR(20) NOT NULL,
   `verified_reason` CHAR(255) NOT NULL,
   `description` CHAR(255) NOT NULL,
   `container_id` CHAR(255) NOT NULL,
   `domain` INT NOT NULL,
   `created_date` TIMESTAMP,
   PRIMARY KEY ( `id` ),
   UNIQUE KEY `uidx_description` (`description`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE follow_details;

CREATE TABLE IF NOT EXISTS `follow_details` (
   `id` INT UNSIGNED AUTO_INCREMENT,
   `user_id` BIGINT NOT NULL,
   `followers_count` INT NOT NULL,
   `follow_count` INT NOT NULL,
   `statuses_count` INT NOT NULL,
   `created_date` TIMESTAMP,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE weibo_details;

CREATE TABLE IF NOT EXISTS `weibo_details` (
   `id` INT UNSIGNED AUTO_INCREMENT,
   `user_id` BIGINT NOT NULL,
   `item_id` CHAR(255) NOT NULL,
   `scheme` CHAR(255) NOT NULL,
   `source` CHAR(50) NOT NULL,
   `reposts_count` CHAR(50) NOT NULL,
   `comments_count` CHAR(50) NOT NULL,
   `attitudes_count` CHAR(50) NOT NULL,
   `text` TEXT NOT NULL,
   `image_content` LONGTEXT NOT NULL,
   `large_image_url` CHAR(255) NOT NULL,
   `weibo_created_at` CHAR(255) NOT NULL,
   `created_date` TIMESTAMP,
   PRIMARY KEY ( `id` ),
   UNIQUE KEY `uidx_item_id` (`item_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT * FROM user_details;
SELECT * FROM follow_details;
SELECT * FROM weibo_details;

-- Update table
ALTER TABLE weibo_details ADD COLUMN region_name CHAR(255) AFTER source;

ALTER TABLE `follow_details` CHANGE `followers_count` `followers_count` CHAR(50);
