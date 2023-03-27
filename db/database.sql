PRAGMA foreign_keys = ON;

.mode box

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS roles;


CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,      
    lastName TEXT NOT NULL,
    name TEXT  NOT NULL,
    email TEXT  NOT NULL UNIQUE,
    phoneNumber TEXT  NOT NULL,
    role INTEGER NOT NULL,
);

CREATE TABLE IF NOT EXISTS products 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,      
    label TEXT NOT NULL UNIQUE,
    image TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description NOT NULL,
);

CREATE TABLE IF NOT EXISTS roles 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,      
    type TEXT NOT NULL UNIQUE,
);

CREATE UNIQUE INDEX email_id 
ON users(email);

CREATE TRIGGER IF NOT EXISTS validate_email
   BEFORE INSERT ON users
BEGIN
   SELECT
      CASE
    WHEN NEW.email NOT LIKE '%_@__%.__%' THEN
         RAISE (ABORT,'Invalid email address')
       END;
END;

INSERT INTO users (lastName, name, email, phoneNumber, role)
 VALUES
 ('Admin', 'admin', 'celladminier@gmail.com', '0605040856', 1),
 ('Aimée', 'Camille', 'aimecamille@free.fr', '0785986325', 1),
 ('Souchon', 'Mathilde', 'souchonmathilde@gmail.com', '0632574896', 2),
 ('Trintignant', 'Arlette', 'arlettetri@icloud.com', '0635487519', 2),
 ('Haillet', 'Cécile', 'cecileh@aol.fr', '0602658974', 2),
 ('Silvestre', 'Patricia', 'patriciasil@isol.net', '078597465', 2),
 ('Calvet', 'Nicole', 'calvet85@epita.eu', '0795680215', 2),
 ('Gueguen', 'Dylan', 'gueguendylan@gmail.com', '0636547852', 2),
 ('Droz', 'Nina', 'droz78@gmail.com', '0602654875', 2),
 ('Corriveau', 'Caroline', 'corriveaucaro@yahoo.fr', '0669587423', 2),
 ('Schaeffer', 'Arthur', 'arthurschae@gmail.com', '0602458645', 2),
 ('Vandame', 'Jérémie', 'jeremvan@gmail.com', '0698745682', 2),
 ('Appell', 'Enzo', 'enzodu69@free.fr', '0789546287', 2),
 ('Cerfbeer', 'Nancy', 'nancy47@gmail.com', '0785496820', 2);

 INSERT INTO products (label, image, price, description)
 VALUES
 ('T-shirt', 'https://picsum.photos/200', 12.5, 'un joli t-shirt'),
 ('Basket', 'https://picsum.photos/200', 45, 'des jolies baskets'),
 ('Casquette', 'https://picsum.photos/200', 10.5, 'une jolie casquette'),
 ('Pantalon', 'https://picsum.photos/200', 35, 'un joli pantalon'),
 ('Chaussettes', 'https://picsum.photos/200', 7, 'une jolie paire de chaussettes'),
 ('Veste', 'https://picsum.photos/200', 75, 'un jolie veste'),

 INSERT INTO roles (type)
 VALUES
 ('admin'),
 ('user'),