### Postman collection is in the repository!

## 🚀 Installation

Follow these steps to set up the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/Prakash5209/personal-todo-fastapi.git
cd personal-todo-fastapi
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_db
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
```

> Replace `your_user`, `your_password`, `your_db`, and `your_jwt_secret` with actual values.

### 5. Run Alembic migrations

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uvicorn app.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI

## 🔐 API Endpoints

### ➕ Register User

`POST /create-account`

**Request Body:**

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "Johndoe@123"
}
```

**Validations:**

- Email must be in a valid format.
- Password must be 5-10 characters and include:
  - at least one uppercase
  - one lowercase
  - one digit
  - one special character

**Response:**

```json
{
  "email": "john@example.com"
}
```

---

### 🔐 Get JWT Token

`POST /get-token`

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "Johndoe@123"
}
```

**Response:**

```json
{
  "token": "<your_jwt_token>"
}
```

---

### 🔁 Update Email

`PUT /update-email`

**Headers:**

```
Authorization: Bearer <your_jwt_token>
```

**Request Body:**

```json
{
  "email": "newemail@example.com"
}
```

**Response:**

```json
{
  "message": "Email updated successfully.",
  "warning": "Please get a new JWT token due to change in email.",
  "updated_email": "newemail@example.com"
}
```

---
---
---
---
> ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

### THIS was just created to clear the database todo list (childs) when deleting users
### THIS was not included in Technical Assessment
### IGNORE THIS
### ❌ Delete User (Admin/Test Only)

`DELETE /delete-user/{id}`

> ⚠️ Use with caution — this deletes the user and their todos (if linked)

**Response:**

```json
{
  "status": 200,
  "message": "User deleted successfully"
}
```



## ✅ todo Management API Tutorial

This section covers how to manage **TODO** using secure JWT-authenticated routes.

All endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <your_token_here>
```

---

### 📌 1. Create a New todo

**Endpoint:** `POST /new-todo`

**Description:** Creates a new todo associated with the authenticated user.

**Request Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "todo": "Complete the assignment"
}
```

**Response:**

```json
{
  "status": 201,
  "content": "new todo added"
}
```

---

### 📌 2. Get List of todos

**Endpoint:** `GET /get-todo?skip=0&limit=10`

**Description:** Retrieves a list of todos for the authenticated user with pagination support.

**Query Parameters:**

- `skip`: number of todos to skip
- `limit`: number of todos to fetch

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "todo": "Complete the assignment",
    "is_completed": false,
    "user_id": 2,
    "created_at": "2025-07-11T12:00:00",
    "updated_at": "2025-07-11T12:00:00"
  },
  ...
]
```

---

### 📌 3. Update a todo

**Endpoint:** `PATCH  /update-todo/{id}`

**Description:** Updates a todo (both content and completion status) of the authenticated user.

**Path Parameter:**

- `id`: todo ID to update

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "todo": "Review code",
  "is_completed": true
}
```

**Response:**

```json
{
  "id": 1,
  "todo": "Review code",
  "is_completed": true,
  "user_id": 2,
  "created_at": "2025-07-11T12:00:00",
  "updated_at": "2025-07-11T13:45:00"
}
```

---

### 📌 4. Delete a todo

**Endpoint:** `DELETE /delete-todo/{id}`

**Description:** Deletes a specific todo of the authenticated user.

**Path Parameter:**

- `id`: todo ID to delete

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response:**

```json
{
  "status": 200,
  "message": "todo deleted successfully"
}
```

---

## 📦 Todo Flow Diagram (Simplified)

```text
Create todo ──▶ DB Save ──▶ Confirmation ✅
    ↑
   JWT

Get todos ──▶ DB Query by user ID ──▶ List of todos
    ↑
   JWT

Update todo ──▶ todo Ownership Check ──▶ Update Fields ──▶ Save
    ↑
   JWT

Delete todo ──▶ todo Ownership Check ──▶ DB Delete ──▶ Success Message
    ↑
   JWT
```

---

## 🛠️ Schema Validations

### ✅ CreatetodoSchema

- `todo`: `str` (required)

### ✅ UpdatetodoSchema

- `todo`: `str`
- `is_completed`: `bool`

---

## 📎 Notes

- All routes are protected using a JWT token.
- todos are always linked to the user who created them.
- Pagination is implemented using `skip` and `limit`.

---


