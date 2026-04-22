# 🔧 Service Ticket Management API

A RESTful API built with Flask that manages customers, service tickets, mechanics, and inventory.
This project demonstrates relational database design, JWT authentication, and advanced relationships using SQLAlchemy.

---

## 🚀 Features

* 🔐 JWT Authentication (login & protected routes)
* 👤 Customer management
* 🧾 Service ticket creation and tracking
* 👨‍🔧 Assign/remove mechanics to tickets
* 📦 Inventory management (parts)
* 🔗 Many-to-many relationships:

  * Tickets ↔ Mechanics
  * Tickets ↔ Inventory (with quantity)
* 📊 Pagination support
* ⚡ Caching and rate limiting
* 🧠 Clean serialization with Marshmallow

---

## 🏗️ Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* Marshmallow
* MySQL
* JWT (python-jose / PyJWT)
* Flask-Limiter
* Flask-Caching

---

## 📂 Project Structure

```
application/
│
├── blueprints/
│   ├── costumers/
│   ├── service_tickets/
│   ├── mechanics/
│   └── inventory/
│
├── models.py
├── extensions.py
├── utils/
│
└── __init__.py
```

---

## 🧠 Database Design

### Main Entities

* **Costumer**
* **ServiceTicket**
* **Mechanic**
* **Inventory**

### Relationships

* One-to-Many:

  * Customer → Service Tickets

* Many-to-Many:

  * ServiceTicket ↔ Mechanic

* Many-to-Many with extra field:

  * ServiceTicket ↔ Inventory
    (via `ServiceTicketInventory`, includes `quantity`)

---

## 🔑 Authentication

JWT-based authentication is used.

### Example Header

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### 👤 Customers

* `POST /costumers` → Create customer
* `GET /costumers` → Get all (pagination supported)
* `PUT /costumers/` → Update current user
* `DELETE /costumers/` → Delete current user

---

### 🧾 Service Tickets

* `POST /service_tickets` → Create ticket
* `GET /service_tickets` → Get all tickets
* `GET /service_tickets/my_tickets` → Get current user tickets
* `PUT /service_tickets/<id>/assign_mechanic/<mechanic_id>`
* `PUT /service_tickets/<id>/remove_mechanic/<mechanic_id>`
* `PUT /service_tickets/<id>/add_part/<inventory_id>` → Add part with quantity
* `DELETE /service_tickets/<id>`

---

### 👨‍🔧 Mechanics

* `POST /mechanics`
* `GET /mechanics`
* `GET /mechanics/search?name=...`
* `GET /mechanics/most-active` → Sorted by number of tickets

---

### 📦 Inventory

* `POST /inventory`
* `GET /inventory`
* `GET /inventory/<id>`
* `PUT /inventory/<id>`
* `DELETE /inventory/<id>`

---

## 📊 Example Response

### Get Tickets with Parts

```json
{
  "total": 2,
  "tickets": [
    {
      "id": 1,
      "service_desc": "Oil change",
      "parts": [
        {
          "quantity": 2,
          "inventory": {
            "name": "Brake Pad",
            "price": 49.99
          }
        }
      ]
    }
  ]
}
```

---

## ⚙️ Setup Instructions

### 1. Clone repo

```
git clone <your-repo-url>
cd project-folder
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure database

Update your connection string:

```python
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://user:password@localhost/db_name"
```

### 5. Run the app

```
python app.py
```

---

## 🧪 Testing

You can test endpoints using:

* Postman
* Thunder Client
* curl

---

## 🧠 Key Concepts Learned

* SQLAlchemy relationships (1:N, M:N, association objects)
* JWT authentication flow
* Schema validation with Marshmallow
* Pagination & API structuring
* RESTful design principles

---

## 📌 Future Improvements

* Role-based authorization (admin/user)
* Unit & integration tests
* Docker setup
* API documentation (Swagger/OpenAPI)

---

## 👨‍💻 Author

Jahvantè Isa Tota
Junior Full-Stack Developer

---
