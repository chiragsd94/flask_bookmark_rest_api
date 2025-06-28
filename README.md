Here's the complete README in a single copy-paste format for your `README.md` file:

---

# 📚 Bookmark REST API

A secure and RESTful Bookmark Management API built using **Flask-RESTX**, **JWT Authentication**, **Flask-SQLAlchemy**, and **Passlib**. This project demonstrates a professional approach to building authenticated APIs with route protection and user-specific access control.

## 🎯 Purpose

> This project is created purely for **educational purposes** and to **demonstrate my skills to potential employers**.
> I am **not liable** for any misuse, data loss, copyright issues, or third-party replication.

## 🚀 Features

- User registration and login
- JWT-based authentication using `Flask-JWT-Extended`
- Secure password hashing using `Passlib`
- CRUD operations for personal bookmarks
- Only logged-in users can perform CRUD operations
- Users can access and modify **only their own** bookmarks
- RESTful API structure with built-in Swagger UI via `Flask-RESTX`

## 🛠️ Technologies Used

- Python 3.x
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Passlib

## 📦 Installation

1. Clone the repository

   ```bash
   git clone https://github.com/chiragsd94/flask_bookmark_rest_api.git
   cd bookmark-api
   ```

2. Create a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables
   Create a `.env` file with the following:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   ```

5. Set flask environment variables
   Create a `.flaskenv` file with the following:

   ```env
   FLASK_APP=api
   FLASK_DEBU=1  # only in development

   ```

6. Run the app

   ```bash
   flask run
   ```

## 🔐 Authentication Flow

1. Register a user
   **POST /api/v1/users/signup**

   ```json
   {
     "email": "user@example.com",
     "password": "yourpassword"
   }
   ```

2. Login to get JWT token
   **POST /api/v1/users/login**

   ```json
   {
     "access_token": "your.jwt.token"
   }
   ```

3. Use the token for all protected routes
   Add this to headers:

   ```
   Authorization: Bearer your.jwt.token
   ```

## 🧾 API Endpoints

### 🔐 Auth

- `POST /api/v1/users/signup` – Register new user
- `POST /api/v1/users/login` – Get JWT token
- `POST /api/v1/users/logout` – Logout User

### 🔖 Bookmarks (Protected)

- `GET /api/v1/bookmarks/` – Get all bookmarks of logged-in user
- `POST /api/v1/bookmarks/` – Add new bookmark
- `GET api/v1/bookmarks/<id>` – Get a specific bookmark
- `PUT api/v1/bookmarks/<id>` – Update a specific bookmark
- `DELETE api/v1/bookmarks/<id>` – Delete a specific bookmark

## ⚠️ Disclaimer

- This project is developed for **educational and demonstration purposes only**.
- I am **not responsible** for any data loss, legal issues, or damages that may arise from using this code.
- All trademarks, logos, and third-party dependencies used belong to their respective owners.

## 🧪 Testing

Test the API using tools like:

- Insomnia
- Postman
- cURL

Make sure to include the JWT token in the `Authorization` header for all protected routes.

- `GET /api/v1/bookmarks/` – Get all bookmarks of logged-in user
- `POST /api/v1/bookmarks/` – Add new bookmark
- `GET api/v1/bookmarks/<id>` – Get a specific bookmark
- `PUT api/v1/bookmarks/<id>` – Update a specific bookmark
- `DELETE api/v1/bookmarks/<id>` – Delete a specific bookmark
- `POST /api/v1/users/logout` – Logout User

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
