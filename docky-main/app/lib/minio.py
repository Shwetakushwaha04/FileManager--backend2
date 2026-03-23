from minio import Minio
from fastapi.responses import StreamingResponse
from uuid import uuid4
import os
from dotenv import load_dotenv
from fastapi import UploadFile
from io import BytesIO

load_dotenv()

minio_client = Minio(
  endpoint=os.getenv("MINIO_ENDPOINT"),
  access_key=os.getenv("MINIO_ACCESS_KEY"),
  secret_key=os.getenv("MINIO_SECRET_KEY"),
  secure=True
)

bucket_name = os.getenv("MINIO_BUCKET")

async def upload_to_minio(file_key: str, content: bytes, content_type: str) -> str:
  

  if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

  #TODO: exception handling
  minio_client.put_object(
    bucket_name,
    file_key,
    data=BytesIO(content),
    length=len(content),
    content_type=content_type
  )

  return True

def download_from_minio(file_key: str):
  #TODO: exception handling
  data = minio_client.get_object(bucket_name, file_key)
  return data
