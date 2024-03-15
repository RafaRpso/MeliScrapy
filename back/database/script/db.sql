/* banco de dados para guardar os dados do mercado livre */
CREATE DATABASE IF NOT EXISTS `mercadolivre`;

CREATE USER 'meli' @'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'mercadoLivre#123';

GRANT ALL PRIVILEGES ON *.* TO 'meli' @'localhost' WITH GRANT OPTION;

ALTER USER 'meli' @'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'mercadoLivre#123';

USE `mercadolivre`;

DROP TABLE IF EXISTS `promotion`;

CREATE TABLE `promotion` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `gross_value` decimal(10, 2) NOT NULL,
    `percent` int NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `meli_id` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `cupom`;

CREATE TABLE `cupom` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `discount` decimal(10, 2) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `price` decimal(10, 2) NOT NULL,
    `category` varchar(255) NOT NULL,
    `image` varchar(1024) NOT NULL,
    `link` varchar(1024) NOT NULL,
    `date` datetime NOT NULL,
    `category` varchar(255) NOT NULL,
    `fk_cupom` int(11) DEFAULT NULL,
    `fk_promotion` int(11),
    FOREIGN KEY (`fk_cupom`) REFERENCES `cupom` (`id`),
    FOREIGN KEY (`fk_promotion`) REFERENCES `promotion` (`id`),
    PRIMARY KEY (`id`) UNIQUE KEY `unique_product` (`title`, `price`, `category`, `image`, `link`)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;