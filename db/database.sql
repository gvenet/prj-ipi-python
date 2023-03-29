PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS roles;
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   lastName TEXT NOT NULL,
   name TEXT NOT NULL,
   email TEXT NOT NULL UNIQUE,
   phoneNumber TEXT NOT NULL,
   role INTEGER NOT NULL,
   password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   label TEXT NOT NULL UNIQUE,
   image TEXT NOT NULL,
   price DECIMAL(10, 2) NOT NULL,
   description NOT NULL
);
CREATE TABLE IF NOT EXISTS roles (
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   type TEXT NOT NULL UNIQUE
);
INSERT INTO products (label, image, price, description)
VALUES (
      'T-shirt',
      'https://assets.laboutiqueofficielle.com/w_450,q_auto,f_auto/media/products/2022/03/17/lbo_310742_SHALBO-2221_20220601T132930_01.jpg',
      12.5,
      'nice t-shirt'
   ),
   (
      'Sneakers',
      'https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/e2bff7de-6d9e-45d2-8fb7-cdab863c8917/chaussure-de-basketball-air-max-impact-3-gVJpX6.png',
      45,
      'nice sneakers'
   ),
   (
      'Cap',
      'https://media.gucci.com/style/DarkGray_Center_0_0_800x800/1519402505/200035_KQWBG_9791_001_100_0000_Light-Casquette-de-base-ball-avec-dtail-bande-Web.jpg',
      10.5,
      'nice cap'
   ),
   (
      'Pant',
      'https://litb-cgis.rightinthebox.com/images/x/202208/bps/product/inc/guzvlr1660517287023.jpg',
      35,
      'pretty pant'
   ),
   (
      'Socks',
      'https://picsum.photos/200',
      7,
      'nice socks'
   ),
   (
      'Jacket',
      'https://picsum.photos/200',
      75,
      'pretty jacket'
   );
INSERT INTO roles (type)
VALUES ('admin'),
   ('user');