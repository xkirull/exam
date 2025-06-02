# Словарь данных системы управления заявками партнеров

## Описание
Данный документ содержит полное описание структуры базы данных системы управления заявками партнеров производственной компании "Новые технологии".

## ER-диаграмма
![ER-диаграмма](er_diagram.png)

## Таблицы базы данных

### 1. partner_types (Типы партнеров)
Справочник типов организационно-правовых форм партнеров.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| type_name | VARCHAR(50) | Название типа партнера | NOT NULL, UNIQUE | ЗАО, ООО, ОАО, ПАО |

**Индексы:**
- PRIMARY KEY (id)
- UNIQUE INDEX (type_name)

---

### 2. partners (Партнеры)
Основная таблица с информацией о партнерах компании.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| partner_type_id | INT | Внешний ключ на тип партнера | NOT NULL, FOREIGN KEY | 2 |
| company_name | VARCHAR(255) | Наименование компании | NOT NULL | Стройдвор |
| director_name | VARCHAR(255) | ФИО директора | NOT NULL | Иванов И.И. |
| email | VARCHAR(255) | Электронная почта | NOT NULL | info@company.ru |
| phone | VARCHAR(20) | Телефон | NOT NULL | +7 495 123 45 67 |
| legal_address | TEXT | Юридический адрес | NOT NULL | г. Москва, ул. Ленина, 1 |
| inn | VARCHAR(20) | ИНН организации | NOT NULL, UNIQUE | 7707123456 |
| rating | INT | Рейтинг партнера | NOT NULL, CHECK (rating >= 0) | 5 |
| logo | LONGBLOB | Логотип компании | NULL | [бинарные данные] |

**Индексы:**
- PRIMARY KEY (id)
- FOREIGN KEY (partner_type_id) REFERENCES partner_types(id)
- UNIQUE INDEX (inn)
- INDEX (company_name)
- INDEX (rating)

**Связи:**
- partner_types (partner_type_id → id) - тип партнера

---

### 3. product_types (Типы продукции)
Справочник типов продукции с коэффициентами для расчетов.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| type_name | VARCHAR(100) | Название типа продукции | NOT NULL, UNIQUE | Плитка |
| coefficient | DECIMAL(10,2) | Коэффициент типа продукции | NOT NULL | 5.25 |

**Индексы:**
- PRIMARY KEY (id)
- UNIQUE INDEX (type_name)

---

### 4. products (Продукция)
Каталог продукции компании.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| product_type_id | INT | Внешний ключ на тип продукции | NOT NULL, FOREIGN KEY | 3 |
| product_name | VARCHAR(255) | Наименование продукции | NOT NULL | Плитка Мозаика 10x10 |
| article | VARCHAR(50) | Артикул продукции | NOT NULL, UNIQUE | 8028248 |
| min_cost_for_partner | DECIMAL(10,2) | Минимальная стоимость для партнера | NOT NULL, CHECK >= 0 | 2500.00 |
| length_cm | DECIMAL(10,2) | Длина в см (параметр 1) | NULL | 10.00 |
| width_cm | DECIMAL(10,2) | Ширина в см (параметр 2) | NULL | 10.00 |

**Индексы:**
- PRIMARY KEY (id)
- FOREIGN KEY (product_type_id) REFERENCES product_types(id)
- UNIQUE INDEX (article)
- INDEX (product_name)

**Связи:**
- product_types (product_type_id → id) - тип продукции

---

### 5. material_types (Типы материалов)
Справочник типов материалов с процентом брака.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| type_name | VARCHAR(100) | Название типа материала | NOT NULL, UNIQUE | Тип материала 1 |
| defect_percentage | DECIMAL(5,4) | Процент брака материала | NOT NULL, CHECK (0-1) | 0.0020 |

**Индексы:**
- PRIMARY KEY (id)
- UNIQUE INDEX (type_name)

---

### 6. partner_requests (Заявки партнеров)
Основная таблица заявок от партнеров.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| partner_id | INT | Внешний ключ на партнера | NOT NULL, FOREIGN KEY | 5 |
| request_date | DATETIME | Дата и время создания заявки | NOT NULL, DEFAULT NOW() | 2024-01-15 10:30:00 |
| status | VARCHAR(50) | Статус заявки | NOT NULL, DEFAULT 'Новая' | Новая |
| total_cost | DECIMAL(12,2) | Общая стоимость заявки | NOT NULL, DEFAULT 0.00, CHECK >= 0 | 25000.00 |

**Индексы:**
- PRIMARY KEY (id)
- FOREIGN KEY (partner_id) REFERENCES partners(id)
- INDEX (request_date)
- INDEX (status)
- INDEX (partner_id, request_date)

**Связи:**
- partners (partner_id → id) - партнер, создавший заявку

**Статусы:**
- Новая - заявка только создана
- В обработке - заявка принята в работу
- Ожидает оплаты - требуется предоплата
- В производстве - продукция производится
- Готова - продукция готова к отгрузке
- Выполнена - заявка закрыта
- Отменена - заявка отменена

---

### 7. request_products (Продукция в заявках)
Связующая таблица между заявками и продукцией.

| Поле | Тип данных | Описание | Ограничения | Пример |
|------|------------|----------|-------------|---------|
| id | INT | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT | 1 |
| request_id | INT | Внешний ключ на заявку | NOT NULL, FOREIGN KEY | 1 |
| product_id | INT | Внешний ключ на продукцию | NOT NULL, FOREIGN KEY | 3 |
| quantity | INT | Количество единиц продукции | NOT NULL, CHECK > 0 | 100 |
| cost_per_unit | DECIMAL(10,2) | Цена за единицу | NOT NULL, CHECK >= 0 | 2500.00 |

**Индексы:**
- PRIMARY KEY (id)
- FOREIGN KEY (request_id) REFERENCES partner_requests(id) ON DELETE CASCADE
- FOREIGN KEY (product_id) REFERENCES products(id)
- UNIQUE INDEX (request_id, product_id)

**Связи:**
- partner_requests (request_id → id) - заявка
- products (product_id → id) - продукция

---

## Представления (Views)

### partner_requests_view
Представление для удобного отображения заявок с информацией о партнерах.

```sql
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
```

### request_products_view
Представление для отображения продукции в заявках с полной информацией.

```sql
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
```

---

## Бизнес-правила и ограничения

1. **Уникальность ИНН**: Каждый партнер должен иметь уникальный ИНН
2. **Рейтинг партнера**: Рейтинг не может быть отрицательным числом
3. **Стоимость продукции**: Минимальная стоимость для партнера не может быть отрицательной
4. **Количество в заявке**: Количество продукции в заявке должно быть положительным целым числом
5. **Уникальность продукции в заявке**: В одной заявке не может быть дублирующихся позиций продукции
6. **Каскадное удаление**: При удалении заявки автоматически удаляются все связанные записи о продукции
7. **Процент брака**: Значение должно быть в диапазоне от 0 до 1 (0% - 100%)
