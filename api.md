# Task Management API Documentation

## Authentication

### Obtain Token
- **URL:** `/token/`
- **Method:** `POST`
- **Description:** Obtain JWT access and refresh tokens.
- **Request Body:**
  - `username`: string
  - `password`: string
- **Response:**
  - `access`: JWT access token
  - `refresh`: JWT refresh token

### Refresh Token
- **URL:** `/token/refresh/`
- **Method:** `POST`
- **Description:** Refresh JWT access token using a refresh token.
- **Request Body:**
  - `refresh`: JWT refresh token
- **Response:**
  - `access`: new JWT access token

---

## Tasks

### List & Create Tasks
- **URL:** `/tasks/`
- **Method:** `GET`, `POST`
- **Description:** 
  - `GET`: List all tasks.
  - `POST`: Create a new task.
- **Request Body (POST):**
  - `title`: string
  - `description`: string
  - `due_date`: date
  - ...other fields as required
- **Response:** Task object(s)

### Create Task (Alternate)
- **URL:** `/tasks/create`
- **Method:** `POST`
- **Description:** Create a new task (same as `/tasks/` POST).
- **Request Body:** Same as above.
- **Response:** Task object

### Update Task
- **URL:** `/tasks/<int:pk>/`
- **Method:** `PUT`, `PATCH`
- **Description:** Update a specific task by ID.
- **Request Body:** Fields to update.
- **Response:** Updated task object

### Task Report
- **URL:** `/tasks/<int:pk>/report/`
- **Method:** `GET`
- **Description:** Get a report for a specific task by ID.
- **Response:** Report data for the task

---

## Users

### Create User
- **URL:** `/users/`
- **Method:** `POST`
- **Description:** Create a new user.
- **Request Body:**
  - `username`: string
  - `password`: string
  - ...other fields as required
- **Response:** User object

### Update User
- **URL:** `/users/<int:pk>/`
- **Method:** `PUT`, `PATCH`
- **Description:** Update a specific user by ID.
- **Request Body:** Fields to update.
- **Response:** Updated user object

---
