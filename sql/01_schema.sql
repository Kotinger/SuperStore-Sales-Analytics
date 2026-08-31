CREATE DATABASE IF NOT EXISTS superstore
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE superstore;

DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS clean_orders;

CREATE TABLE clean_orders (
  order_id VARCHAR(50) NOT NULL,
  order_date DATETIME NOT NULL,
  ship_date DATETIME NOT NULL,
  ship_mode VARCHAR(50) NULL,
  customer_name VARCHAR(255) NULL,
  segment VARCHAR(50) NULL,
  state VARCHAR(100) NULL,
  country VARCHAR(100) NULL,
  market VARCHAR(50) NULL,
  region VARCHAR(50) NULL,
  product_id VARCHAR(50) NULL,
  category VARCHAR(100) NULL,
  sub_category VARCHAR(100) NULL,
  product_name VARCHAR(255) NULL,
  sales DECIMAL(14, 2) NOT NULL,
  quantity INT NOT NULL,
  discount DECIMAL(8, 4) NULL,
  profit DECIMAL(14, 2) NULL,
  shipping_cost DECIMAL(14, 2) NULL,
  order_priority VARCHAR(20) NULL,
  year INT NULL,
  ship_days INT NULL,
  order_key VARCHAR(512) NOT NULL,
  customer_key VARCHAR(512) NULL,
  KEY idx_order_key (order_key),
  KEY idx_customer_key (customer_key),
  KEY idx_order_date (order_date),
  KEY idx_country (country),
  KEY idx_category (category)
) ENGINE=InnoDB;

CREATE TABLE people (
  customer_key VARCHAR(512) NOT NULL PRIMARY KEY,
  orders INT NOT NULL,
  gmv DECIMAL(14, 2) NOT NULL,
  lines INT NOT NULL,
  first_order DATETIME NOT NULL
) ENGINE=InnoDB;
