SET SQL_SAFE_UPDATES = 0;

DROP DATABASE IF EXISTS user2;

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS user2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE user2;

-- Таблица типов партнеров
CREATE TABLE partner_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL UNIQUE
);

-- Таблица партнеров
CREATE TABLE partners (
    id INT PRIMARY KEY AUTO_INCREMENT,
    partner_type_id INT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    director_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    legal_address TEXT NOT NULL,
    inn VARCHAR(20) NOT NULL UNIQUE,
    rating INT NOT NULL CHECK (rating >= 0),
    logo LONGBLOB NULL,
    FOREIGN KEY (partner_type_id) REFERENCES partner_types(id)
);

-- Таблица типов продукции
CREATE TABLE product_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    coefficient DECIMAL(10,2) NOT NULL
);

-- Таблица продукции
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_type_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    article VARCHAR(50) NOT NULL UNIQUE,
    min_cost_for_partner DECIMAL(10,2) NOT NULL CHECK (min_cost_for_partner >= 0),
    length_cm DECIMAL(10,2) NULL,
    width_cm DECIMAL(10,2) NULL,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id)
);

-- Таблица типов материалов
CREATE TABLE material_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    defect_percentage DECIMAL(5,4) NOT NULL CHECK (defect_percentage >= 0 AND defect_percentage <= 1)
);

-- Таблица заявок партнеров
CREATE TABLE partner_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    partner_id INT NOT NULL,
    request_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Новая',
    total_cost DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (total_cost >= 0),
    FOREIGN KEY (partner_id) REFERENCES partners(id)
);

-- Таблица продукции в заявках
CREATE TABLE request_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    request_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    cost_per_unit DECIMAL(10,2) NOT NULL CHECK (cost_per_unit >= 0),
    FOREIGN KEY (request_id) REFERENCES partner_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE KEY unique_request_product (request_id, product_id)
);

-- Вставка типов партнеров
INSERT INTO partner_types (type_name) VALUES 
('ЗАО'), ('ООО'), ('ОАО'), ('ПАО');

-- Вставка типов продукции из импорта
INSERT INTO product_types (type_name, coefficient) VALUES
('Древесно-плитные материалы', 1.5),
('Декоративные панели', 3.5),
('Плитка', 5.25),
('Фасадные материалы', 4.5),
('Напольные покрытия', 2.17);

-- Вставка типов материалов из импорта
INSERT INTO material_types (type_name, defect_percentage) VALUES
('Тип материала 1', 0.002),
('Тип материала 2', 0.005),
('Тип материала 3', 0.003),
('Тип материала 4', 0.0015),
('Тип материала 5', 0.0018);

-- Вставка партнеров из импорта
INSERT INTO partners (partner_type_id, company_name, director_name, email, phone, legal_address, inn, rating)
SELECT 
    pt.id,
    p.company_name,
    p.director_name,
    p.email,
    p.phone,
    p.legal_address,
    p.inn,
    p.rating
FROM (
    SELECT 'ЗАО' as type_name, 'Стройдвор' as company_name, 'Андреева Ангелина Николаевна' as director_name, 'angelina77@kart.ru' as email, '492 452 22 82' as phone, '143001, Московская область, город Одинцово, уд. Ленина, 21' as legal_address, '9432455179' as inn, 5 as rating
    UNION ALL SELECT 'ЗАО', 'Самоделка', 'Мельников Максим Петрович', 'melnikov.maksim88@hm.ru', '812 267 19 59', '306230, Курская область, город Обоянь, ул. 1 Мая, 89', '7803888520', 3
    UNION ALL SELECT 'ООО', 'Деревянные изделия', 'Лазарев Алексей Сергеевич', 'aleksejlazarev@al.ru', '922 467 93 83', '238340, Калининградская область, город Светлый, ул. Морская, 12', '8430391035', 4
    UNION ALL SELECT 'ООО', 'Декор и отделка', 'Саншокова Мадина Муратовна', 'mmsanshokova@lss.ru', '413 230 30 79', '685000, Магаданская область, город Магадан, ул. Горького, 15', '4318170454', 7
    UNION ALL SELECT 'ООО', 'Паркет', 'Иванов Дмитрий Сергеевич', 'ivanov.dmitrij@mail.ru', '921 851 21 22', '606440, Нижегородская область, город Бор, ул. Свободы, 3', '7687851800', 7
    UNION ALL SELECT 'ПАО', 'Дом и сад', 'Аникеева Екатерина Алексеевна', 'ekaterina.anikeeva@ml.ru', '499 936 29 26', '393760, Тамбовская область, город Мичуринск, ул. Красная, 50', '6119144874', 7
    UNION ALL SELECT 'ОАО', 'Легкий шаг', 'Богданова Ксения Владимировна', 'bogdanova.kseniya@bkv.ru', '495 445 61 41', '307370, Курская область, город Рыльск, ул. Гагарина, 16', '1122170258', 6
    UNION ALL SELECT 'ПАО', 'СтройМатериалы', 'Холодова Валерия Борисовна', 'holodova@education.ru', '499 234 56 78', '140300, Московская область, город Егорьевск, ул. Советская, 24', '8355114917', 5
    UNION ALL SELECT 'ОАО', 'Мир отделки', 'Крылов Савелий Тимофеевич', 'stkrylov@mail.ru', '908 713 51 88', '344116, Ростовская область, город Ростов-на-Дону, ул. Артиллерийская, 4', '3532367439', 8
    UNION ALL SELECT 'ОАО', 'Технологии комфорта', 'Белов Кирилл Александрович', 'kirill_belov@kir.ru', '918 432 12 34', '164500, Архангельская область, город Северодвинск, ул. Ломоносова, 29', '2362431140', 4
    UNION ALL SELECT 'ПАО', 'Твой дом', 'Демидов Дмитрий Александрович', 'dademidov@ml.ru', '919 698 75 43', '354000, Краснодарский край, город Сочи, ул. Больничная, 11', '4159215346', 10
    UNION ALL SELECT 'ЗАО', 'Новые краски', 'Алиев Дамир Игоревич', 'alievdamir@tk.ru', '812 823 93 42', '187556, Ленинградская область, город Тихвин, ул. Гоголя, 18', '9032455179', 9
    UNION ALL SELECT 'ОАО', 'Политехник', 'Котов Михаил Михайлович', 'mmkotov56@educat.ru', '495 895 71 77', '143960, Московская область, город Реутов, ул. Новая, 55', '3776671267', 5
    UNION ALL SELECT 'ОАО', 'СтройАрсенал', 'Семенов Дмитрий Максимович', 'semenov.dm@mail.ru', '896 123 45 56', '242611, Брянская область, город Фокино, ул. Фокино, 23', '7447864518', 5
    UNION ALL SELECT 'ПАО', 'Декор и порядок', 'Болотов Артем Игоревич', 'artembolotov@ab.ru', '950 234 12 12', '309500, Белгородская область, город Старый Оскол, ул. Цветочная, 20', '9037040523', 5
    UNION ALL SELECT 'ПАО', 'Умные решения', 'Воронова Анастасия Валерьевна', 'voronova_anastasiya@mail.ru', '923 233 27 69', '652050, Кемеровская область, город Юрга, ул. Мира, 42', '6221520857', 3
    UNION ALL SELECT 'ЗАО', 'Натуральные покрытия', 'Горбунов Василий Петрович', 'vpgorbunov24@vvs.ru', '902 688 28 96', '188300, Ленинградская область, город Гатчина, пр. 25 Октября, 17', '2262431140', 9
    UNION ALL SELECT 'ООО', 'СтройМастер', 'Смирнов Иван Андреевич', 'smirnov_ivan@kv.ru', '917 234 75 55', '184250, Мурманская область, город Кировск, пр. Ленина, 24', '4155215346', 9
    UNION ALL SELECT 'ООО', 'Гранит', 'Джумаев Ахмед Умарович', 'dzhumaev.ahmed@amail.ru', '495 452 55 95', '162390, Вологодская область, город Великий Устюг, ул. Железнодорожная, 36', '3961234561', 5
    UNION ALL SELECT 'ЗАО', 'Строитель', 'Петров Николай Тимофеевич', 'petrov.nikolaj31@mail.ru', '916 596 15 55', '188910, Ленинградская область, город Приморск, ш. Приморское, 18', '9600275878', 10
) p
JOIN partner_types pt ON pt.type_name = p.type_name;

-- Вставка продукции из импорта
INSERT INTO products (product_type_id, product_name, article, min_cost_for_partner)
SELECT 
    pt.id,
    p.product_name,
    p.article,
    p.min_cost_for_partner
FROM (
    SELECT 'Древесно-плитные материалы' as type_name, 'Фанера ФСФ 1800х1200х27 мм бежевая береза' as product_name, '6549922' as article, 5100 as min_cost_for_partner
    UNION ALL SELECT 'Декоративные панели', 'Мягкие панели прямоугольник велюр цвет оливковый 600х300х35 мм', '7018556', 1880
    UNION ALL SELECT 'Фасадные материалы', 'Бетонная плитка Белый кирпич микс 30х7,3 см', '5028272', 2080
    UNION ALL SELECT 'Плитка', 'Плитка Мозаика 10x10 см цвет белый глянец', '8028248', 2500
    UNION ALL SELECT 'Напольные покрытия', 'Ламинат Дуб Античный серый 32 класс толщина 8 мм с фаской', '9250282', 4050
    UNION ALL SELECT 'Декоративные панели', 'Стеновая панель МДФ Флора 1440x500x10 мм', '7130981', 2100.56
    UNION ALL SELECT 'Фасадные материалы', 'Бетонная плитка Красный кирпич 20x6,5 см', '5029784', 2760
    UNION ALL SELECT 'Напольные покрытия', 'Ламинат Канди Дизайн 33 класс толщина 8 мм с фаской', '9658953', 3200.96
    UNION ALL SELECT 'Древесно-плитные материалы', 'Плита ДСП 11 мм влагостойкая 594x1815 мм', '6026662', 497.69
    UNION ALL SELECT 'Напольные покрытия', 'Ламинат с натуральным шпоном Дуб Эксперт толщина 6 мм с фаской', '9159043', 3750
    UNION ALL SELECT 'Плитка', 'Плитка настенная Формат 20x40 см матовая цвет мята', '8588376', 2500
    UNION ALL SELECT 'Древесно-плитные материалы', 'Плита ДСП Кантри 16 мм 900x1200 мм', '6758375', 1050.96
    UNION ALL SELECT 'Декоративные панели', 'Стеновая панель МДФ Сосна Полярная 60х280х4мсм цвет коричневый', '7759324', 1700
    UNION ALL SELECT 'Фасадные материалы', 'Клинкерная плитка коричневая 29,8х29,8 см', '5118827', 860
    UNION ALL SELECT 'Плитка', 'Плитка настенная Цветок 60x120 см цвет зелено-голубой', '8559898', 2300
    UNION ALL SELECT 'Декоративные панели', 'Пробковое настенное покрытие 600х300х3 мм белый ', '7259474', 3300
    UNION ALL SELECT 'Плитка', 'Плитка настенная Нева 30x60 см цвет серый', '8115947', 1700
    UNION ALL SELECT 'Фасадные материалы', 'Гипсовая плитка настенная Дом на берегу кирпич белый 18,5х4,5 см', '5033136', 499
    UNION ALL SELECT 'Напольные покрытия', 'Ламинат Дуб Северный белый 32 класс толщина 8 мм с фаской', '9028048', 2550
    UNION ALL SELECT 'Древесно-плитные материалы', 'Дерево волокнистая плита Дуб Винтаж 1200х620х3 мм светло-коричневый', '6123459', 900.5
) p
JOIN product_types pt ON pt.type_name = p.type_name;

DROP table IF EXISTS temp_partner_requests;

-- Создание временной таблицы для импорта заявок
CREATE TEMPORARY TABLE IF NOT EXISTS temp_partner_requests (
    product_name VARCHAR(255),
    partner_name VARCHAR(255),
    quantity INT
);

-- Вставка данных из Partner_products_request_import
INSERT INTO temp_partner_requests (product_name, partner_name, quantity) VALUES
('Плитка Мозаика 10x10 см цвет белый глянец', 'Стройдвор', 2000),
('Ламинат Дуб Античный серый 32 класс толщина 8 мм с фаской', 'Самоделка', 3000),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'Деревянные изделия', 1000),
('Бетонная плитка Белый кирпич микс 30х7,3 см', 'Декор и отделка', 9500),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'Паркет', 2000),
('Гипсовая плитка настенная Дом на берегу кирпич белый 18,5х4,5 см', 'Дом и сад', 1100),
('Плита ДСП Кантри 16 мм 900x1200 мм', 'Легкий шаг', 5000),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'СтройМатериалы', 2500),
('Мягкие панели прямоугольник велюр цвет оливковый 600х300х35 мм', 'Мир отделки', 6000),
('Стеновая панель МДФ Флора 1440x500x10 мм', 'Технологии комфорта', 7000),
('Плитка Мозаика 10x10 см цвет белый глянец', 'Твой дом', 5000),
('Плитка Мозаика 10x10 см цвет белый глянец', 'Новые краски', 7500),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'Политехник', 3000),
('Гипсовая плитка настенная Дом на берегу кирпич белый 18,5х4,5 см', 'СтройАрсенал', 500),
('Пробковое настенное покрытие 600х300х3 мм белый ', 'Декор и порядок', 7000),
('Плита ДСП 11 мм влагостойкая 594x1815 мм', 'Умные решения', 4000),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'Натуральные покрытия', 3500),
('Фанера ФСФ 1800х1200х27 мм бежевая береза', 'СтройМастер', 7900),
('Плитка настенная Цветок 60x120 см цвет зелено-голубой', 'Гранит', 9600),
('Плитка настенная Цветок 60x120 см цвет зелено-голубой', 'Строитель', 1200);

-- Создание заявок и добавление продукции в них
INSERT INTO partner_requests (partner_id, request_date, status)
SELECT DISTINCT p.id, NOW(), 'Новая'
FROM temp_partner_requests tpr
JOIN partners p ON p.company_name = tpr.partner_name;

-- Добавление продукции в заявки
INSERT INTO request_products (request_id, product_id, quantity, cost_per_unit)
SELECT 
    pr.id,
    prod.id,
    tpr.quantity,
    prod.min_cost_for_partner
FROM temp_partner_requests tpr
JOIN partners p ON p.company_name = tpr.partner_name
JOIN partner_requests pr ON pr.partner_id = p.id
JOIN products prod ON prod.product_name = tpr.product_name;

-- Обновление общей стоимости заявок
UPDATE partner_requests pr
SET total_cost = (
    SELECT ROUND(SUM(rp.quantity * rp.cost_per_unit), 2)
    FROM request_products rp
    WHERE rp.request_id = pr.id
);

-- Создание индексов для оптимизации
CREATE INDEX idx_partner_requests_partner_id ON partner_requests(partner_id);
CREATE INDEX idx_request_products_request_id ON request_products(request_id);
CREATE INDEX idx_request_products_product_id ON request_products(product_id);
CREATE INDEX idx_products_product_type_id ON products(product_type_id);

-- Представление для просмотра заявок с информацией о партнере
CREATE VIEW partner_requests_view AS
SELECT 
    pr.id as request_id,
    pr.request_date,
    pr.status,
    pr.total_cost,
    p.id as partner_id,
    pt.type_name as partner_type,
    p.company_name,
    p.director_name,
    p.email,
    p.phone,
    p.legal_address,
    p.inn,
    p.rating
FROM partner_requests pr
JOIN partners p ON pr.partner_id = p.id
JOIN partner_types pt ON p.partner_type_id = pt.id;

-- Представление для просмотра продукции в заявках
CREATE VIEW request_products_view AS
SELECT 
    rp.request_id,
    rp.id as request_product_id,
    prod.id as product_id,
    prod.product_name,
    prod.article,
    rp.quantity,
    rp.cost_per_unit,
    ROUND(rp.quantity * rp.cost_per_unit, 2) as total_product_cost,
    pt.type_name as product_type
FROM request_products rp
JOIN products prod ON rp.product_id = prod.id
JOIN product_types pt ON prod.product_type_id = pt.id;

DROP TEMPORARY TABLE IF EXISTS temp_partner_requests;
