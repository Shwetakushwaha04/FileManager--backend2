import io
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from PIL import Image

from app.lib import upload_to_minio, download_from_minio, gcu
from app.models import Document, Folder

router = APIRouter()

def create_thumbnail(image_bytes: bytes, size=(64, 64)) -> bytes:
  img = Image.open(io.BytesIO(image_bytes))
  img.thumbnail(size)
  out = io.BytesIO()
  img.save(out, format="PNG")
  return out.getvalue()

  
@router.post("/upload/{parent_uuid}")
async def upload_file_to_a_folder(file: UploadFile = File(...), parent_uuid: str = None, user: gcu = None):  # type: ignore
  try:
    file_id = uuid4()
    content = await file.read()
    content_type = file.content_type

    parent = await Folder.get_or_none(uuid=parent_uuid)
    if not parent:
      parent_uuid = None  # If no parent folder is specified, set to None
    elif parent.owner_id != user.id:
      raise HTTPException(status_code=403, detail="You do not have permission to create a folder in this parent folder")
    
    is_uploaded = await upload_to_minio(str(file_id), content, content_type)
    
    thumb_bytes = None
    if content_type.startswith("image/"):
      # Create a thumbnail if the file is an image
      thumb_bytes = create_thumbnail(content)

    obj = await Document.create(uuid=file_id, name=file.filename, type=file.content_type, size=file.size, owner_id=user.id, folder_id=parent_uuid, thumbnail_blob=thumb_bytes)
    return Response(status_code=201)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_id}")
async def download_file(file_id: str, user: gcu = None):
  try:
    obj = await Document.get_or_none(uuid=file_id)  # Ensure the file exists
    if not obj:
      raise HTTPException(status_code=404, detail="File not found")
    elif obj.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to download this file")
    # Download the file from MinIO
    response = download_from_minio(file_id)
    return StreamingResponse(response, media_type=obj.type, headers={"Content-Disposition": f"attachment; filename={obj.name}"})
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

@router.get("/thumbnail/{file_id}")
async def get_thumbnail(file_id: str, user: gcu = None):
  try:
    obj = await Document.get_or_none(uuid=file_id)  # Ensure the file exists
    if not obj:
      raise HTTPException(status_code=404, detail="File not found")
    elif obj.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this thumbnail")
    
    if not obj.thumbnail_blob:
      raise HTTPException(status_code=404, detail="Thumbnail not available for this file")

    return StreamingResponse(io.BytesIO(obj.thumbnail_blob), media_type="image/png")
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))
