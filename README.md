# Blog APIs

A RESTful API for a blogging platform built with Flask and SQLAlchemy. This application provides a complete backend for managing users, blog posts, and comments.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Data Seeding](#data-seeding)
- [Usage Examples](#usage-examples)

## ✨ Features

- **User Management**: Create, read, update, and delete user accounts
- **Blog Posts**: Users can create and manage blog posts
- **Comments**: Users can comment on blog posts
- **Password Security**: Passwords are hashed using werkzeug security utilities
- **Database Relationships**: Proper relational database structure with cascading deletes
- **Data Seeding**: Automated database population with fake data using Faker library

## 🛠️ Tech Stack

- **Framework**: Flask
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database**: SQLite (blog.db)
- **Security**: Werkzeug (password hashing)
- **Data Generation**: Faker

## 📁 Project Structure

```
blog-APIs/
├── app.py           # Main Flask application and API endpoints
├── models.py        # SQLAlchemy database models
├── extension.py     # SQLAlchemy extension initialization
├── seeding.py       # Database seeding script
└── README.md        # This file
```

## 💾 Database Models

### User Model
- `id` (Integer, Primary Key)
- `username` (String, Unique, Required)
- `email` (String, Unique, Required)
- `hashed_password` (String, Required)
- Relationships: Posts and Comments

### Post Model
- `id` (Integer, Primary Key)
- `title` (String, Required)
- `content` (Text, Required)
- `author_id` (Foreign Key to User)
- Relationships: Comments

### Comment Model
- `id` (Integer, Primary Key)
- `content` (Text, Required)
- `author_id` (Foreign Key to User)
- `post_id` (Foreign Key to Post)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mostafa-12/blog-APIs
   cd blog-APIs
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy werkzeug faker
   ```

## ▶️ Running the Application

1. **Start the Flask application**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **Seed the database with sample data** (optional)
   ```bash
   python seeding.py
   ```
   This creates 10 users, 20 posts, and 50 comments with random data.

## 📡 API Endpoints

### Users

- **GET** `/users` - Retrieve all users
- **POST** `/users` - Create a new user
  - Request body: `{"username": "string", "email": "string", "password": "string"}`
- **GET** `/users/<user_id>` - Retrieve a specific user (if implemented)
- **PUT** `/users/<user_id>` - Update a user completely
  - Request body: `{"username": "string", "email": "string", "password": "string"}`
- **PATCH** `/users/<user_id>` - Partially update a user
  - Request body: `{"username": "string"}` (any field combination)
- **DELETE** `/users/<user_id>` - Delete a user

### Response Codes

- `200` - Success (GET, PUT, PATCH)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (error processing)
- `404` - Not Found (user doesn't exist)

## 📚 Usage Examples

### Create a User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "secure123"}'
```

### Get All Users
```bash
curl http://localhost:5000/users
```

### Update a User (Complete)
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_doe", "email": "jane@example.com", "password": "newsecure123"}'
```

### Partially Update a User
```bash
curl -X PATCH http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

### Delete a User
```bash
curl -X DELETE http://localhost:5000/users/1
```

## 🌱 Data Seeding

The `seeding.py` script populates the database with sample data:

```bash
python seeding.py
```

This will create:
- 10 random users with fake names, emails, and passwords
- 20 random blog posts with titles and content
- 50 random comments associated with random users and posts

## 📝 Notes

- Passwords are never stored in plain text; they are hashed using werkzeug's security functions
- The `password` property on the User model is write-only for security reasons
- All database operations include error handling with rollback on failure
- Foreign key constraints with cascade delete ensure referential integrity
