# inventory_order_management
>>A backend-focused Inventory and Order Management System built using Python and MySQL.
The project emphasizes clean architecture, transaction safety, and database-level business rule enforcement, similar to real production backend systems.

>>Features
Product inventory management with real-time stock tracking
Order placement with transaction handling and rollback support
Prevention of overselling using database-level validations
Stored procedures, triggers, and row locking for data integrity
Clean separation of models, services, and utilities
End-to-end testing using Python service layer

 >>Tech Stack
Language: Python
Database: MySQL

>>Concepts Used:
OOP (Models & Services)
Transactions & Rollbacks
Stored Procedures
Triggers
DSA concepts (structured logic, validations)

>>Project Structure
inventory_order_management/
├── src/
│   ├── main.py
│   ├── test_flow.py
│   ├── utils/
│   │   └── db_connection.py
│   ├── models/
│   │   └── product.py
│   └── services/
│       ├── inventory_service.py
│       └── order_service.py
└── README.md

>>Database Design
Tables: products, orders, customers
Stored Procedure:Handles order placement
Checks stock availability
Uses transactions and row locking
Triggers:Automatically update inventory on order creation
