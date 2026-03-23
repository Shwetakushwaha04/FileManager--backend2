import os
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
  "connections": {
    "default": os.getenv("DB_URL")
  },
  "apps": {
    "models": {
      "models": ["app.models"],  # your models + aerich
      "default_connection": "default",
    },
  },
}

def init_db(app: FastAPI) -> None:
  register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Automatically generate tables
    add_exception_handlers=True,
  )

Tortoise.init_models(["app.models"], "models")
