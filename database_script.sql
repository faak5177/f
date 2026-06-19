-- ============================================================
-- Demoekzamen / вариант 3 / схема БД
-- ============================================================

BEGIN;

DROP TABLE IF EXISTS "Orders"        CASCADE;
DROP TABLE IF EXISTS "PickPoints"    CASCADE;
DROP TABLE IF EXISTS "Products"      CASCADE;
DROP TABLE IF EXISTS "Suplyers"      CASCADE;
DROP TABLE IF EXISTS "Manufactures"  CASCADE;
DROP TABLE IF EXISTS "Categories"    CASCADE;
DROP TABLE IF EXISTS "Users"         CASCADE;
DROP TABLE IF EXISTS "Roles"         CASCADE;

CREATE TABLE "Roles" (
    role_id   SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "Users" (
    user_id     SERIAL PRIMARY KEY,
    surname     VARCHAR(60)  NOT NULL,
    name        VARCHAR(60)  NOT NULL,
    patronymic  VARCHAR(60),
    login       VARCHAR(40)  NOT NULL UNIQUE,
    password    VARCHAR(120) NOT NULL,
    role_id     INTEGER NOT NULL REFERENCES "Roles"(role_id)
);

CREATE TABLE "Categories" (
    category_id   SERIAL PRIMARY KEY,
    category_name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE "Manufactures" (
    manufacture_id   SERIAL PRIMARY KEY,
    manufacture_name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE "Suplyers" (
    suplyer_id   SERIAL PRIMARY KEY,
    suplyer_name VARCHAR(120) NOT NULL,
    inn          VARCHAR(12)  NOT NULL UNIQUE,
    address      VARCHAR(200)
);

CREATE TABLE "Products" (
    article         VARCHAR(20) PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    unit            VARCHAR(20),
    price           NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    max_discount    INTEGER CHECK (max_discount BETWEEN 0 AND 100),
    manufacture_id  INTEGER REFERENCES "Manufactures"(manufacture_id),
    suplyer_id      INTEGER REFERENCES "Suplyers"(suplyer_id),
    category_id     INTEGER REFERENCES "Categories"(category_id),
    discount        INTEGER DEFAULT 0 CHECK (discount BETWEEN 0 AND 100),
    quantity        INTEGER DEFAULT 0 CHECK (quantity >= 0),
    description     TEXT,
    image_path      VARCHAR(255)
);

CREATE TABLE "PickPoints" (
    pickpoint_id SERIAL PRIMARY KEY,
    address      VARCHAR(200) NOT NULL
);

CREATE TABLE "Orders" (
    order_id        SERIAL PRIMARY KEY,
    pickpoint_id    INTEGER REFERENCES "PickPoints"(pickpoint_id),
    order_date      DATE     NOT NULL DEFAULT CURRENT_DATE,
    delivery_date   DATE,
    status          VARCHAR(30) NOT NULL DEFAULT 'Новый',
    user_id         INTEGER REFERENCES "Users"(user_id),
    article         VARCHAR(20) REFERENCES "Products"(article),
    quantity        INTEGER NOT NULL DEFAULT 1,
    pickup_code     INTEGER
);

CREATE INDEX idx_products_category   ON "Products"(category_id);
CREATE INDEX idx_products_manufact   ON "Products"(manufacture_id);
CREATE INDEX idx_orders_user         ON "Orders"(user_id);
CREATE INDEX idx_orders_article      ON "Orders"(article);
CREATE INDEX idx_users_login         ON "Users"(login);

COMMIT;
