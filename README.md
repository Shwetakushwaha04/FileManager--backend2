# File Manager Backend improved version

## Overview
Docky is a backend file management system built using FastAPI. It provides APIs for managing users, folders, and files with secure authentication and object storage integration.

## 🛠️ Tech Stack
- FastAPI
- Tortoise ORM
- JWT Authentication
- MinIO (Object Storage)
- Python

## Features
- User authentication using JWT
- Folder creation and nested structure
- File upload and management
- Document handling APIs
- Secure route protection
- Scalable backend architecture

## Project Structure
- `models/` → Database models
- `schemas/` → Request/response schemas
- `routers/` → API routes
- `auth/` → Authentication logic

## ⚙️ How to Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
