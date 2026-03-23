from fastapi import APIRouter, HTTPException, Response
from app.models import Document, Folder
from app.schemas import DocumentPydanticSlim, DocumentInPydantic
from app.lib import gcu

router = APIRouter()

@router.get("", response_model=list[DocumentPydanticSlim])
async def list_documents(user: gcu): # type: ignore
  return await DocumentPydanticSlim.from_queryset(Document.filter(owner_id=user.id))
