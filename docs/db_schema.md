# Схема базы данных (PostgreSQL)

```mermaid
erDiagram
    Roles ||--o{ Users : has
    Categories ||--o{ Products : categorises
    Manufactures ||--o{ Products : produces
    Suplyers ||--o{ Products : supplies
    Products ||--o{ Orders : contains
    PickPoints ||--o{ Orders : delivers_to
    Users ||--o{ Orders : places

    Roles {
        int role_id PK
        varchar role_name
    }
    Users {
        int user_id PK
        varchar surname
        varchar name
        varchar patronymic
        varchar login UK
        varchar password
        int role_id FK
    }
    Categories {
        int category_id PK
        varchar category_name
    }
    Manufactures {
        int manufacture_id PK
        varchar manufacture_name
    }
    Suplyers {
        int suplyer_id PK
        varchar suplyer_name
        varchar inn UK
        varchar address
    }
    Products {
        varchar article PK
        varchar name
        varchar unit
        numeric price
        int max_discount
        int manufacture_id FK
        int suplyer_id FK
        int category_id FK
        int discount
        int quantity
        text description
        varchar image_path
    }
    PickPoints {
        int pickpoint_id PK
        varchar address
    }
    Orders {
        int order_id PK
        int pickpoint_id FK
        date order_date
        date delivery_date
        varchar status
        int user_id FK
        varchar article FK
        int quantity
        int pickup_code
    }
```

## Ключевые ограничения

- `Products.price` — `NUMERIC(12,2)`, `CHECK price >= 0`.
- `Products.discount`, `Products.max_discount` — `CHECK BETWEEN 0 AND 100`.
- `Products.quantity` — `CHECK quantity >= 0`.
- `Orders.order_date` — `NOT NULL DEFAULT CURRENT_DATE`.
- `Orders.status` — `NOT NULL DEFAULT 'Новый'`.
- Индексы: `Products(category_id)`, `Products(manufacture_id)`, `Orders(user_id)`, `Orders(article)`, `Users(login)`.
