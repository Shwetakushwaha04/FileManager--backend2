# File Manager Backend improved 

## Overview
Docky is a backend file management system built using FastAPI. It allows users to securely manage folders and files with authentication and scalable object storage.

This project follows a modular backend architecture with clear separation of models, schemas, and API routes.

---

## 🛠️ Tech Stack
- FastAPI (Backend Framework)
- Tortoise ORM (Database ORM)
- JWT (Authentication)
- MinIO (Object Storage)
- Python

##  Core Features

### 1. Authentication System
- User signup & login
- JWT-based authentication (stateless)
- Secure route protection using tokens

### 2. Folder Management
- Create folders
- Nested folder structure
- Organized file storage

### 3. File & Document Handling
- Upload files
- Store file metadata (name, type, size, etc.)
- Manage documents via APIs

### 4. Storage Integration
- MinIO used for scalable object storage
- Files stored separately from metadata
- Efficient file retrieval system



##  Architecture Explanation

The project is structured in a clean and scalable way:

- `models/` → Database tables (User, Folder, File, Document)
- `schemas/` → Data validation & API request/response models
- `routers/` → API endpoints (auth, folder, file, etc.)
- `auth/` → JWT authentication logic

This separation ensures:
- Clean code
- Easy scalability
- Maintainability


## API Flow 

1. User sends login request
2. Server validates credentials
3. JWT token is generated
4. Frontend stores token
5. Token is sent in headers for protected routes
6. Backend verifies token → allows access

---

## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
