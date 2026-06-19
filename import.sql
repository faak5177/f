-- ============================================================
--  Demoekzamen / вариант 3 / импорт CSV (PostgreSQL)
--  Выполнять в psql, находясь в корне проекта.
-- ============================================================

\copy "Roles"(role_name)                                              FROM 'Роли.csv'           DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "Categories"(category_name)                                     FROM 'Категории.csv'      DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "Manufactures"(manufacture_name)                                FROM 'Производители.csv'  DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "Suplyers"(suplyer_name, inn, address)                          FROM 'Поставщики.csv'     DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "Users"(surname, name, patronymic, login, password, role_id)    FROM 'Пользователи.csv'   DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "Products"(article, name, unit, price, max_discount, manufacture_id, suplyer_id, category_id, discount, quantity, description, image_path) FROM 'Товары.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
\copy "PickPoints"(address)                                           FROM 'Точки подбора.csv'  DELIMITER ';' CSV HEADER ENCODING 'UTF8';

-- проверка количеств
SELECT 'Roles' AS t, COUNT(*) FROM "Roles"
UNION ALL SELECT 'Categories',   COUNT(*) FROM "Categories"
UNION ALL SELECT 'Manufactures', COUNT(*) FROM "Manufactures"
UNION ALL SELECT 'Suplyers',     COUNT(*) FROM "Suplyers"
UNION ALL SELECT 'Users',        COUNT(*) FROM "Users"
UNION ALL SELECT 'Products',     COUNT(*) FROM "Products"
UNION ALL SELECT 'PickPoints',   COUNT(*) FROM "PickPoints";
