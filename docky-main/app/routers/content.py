from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.models import Document, Folder
from app.schemas import DocumentPydanticSlim, FolderPydanticSlim
from app.lib import gcu

router = APIRouter()

class FolderContents(BaseModel):
  folders: List[FolderPydanticSlim] # type: ignore
  documents: List[DocumentPydanticSlim] # type: ignore

@router.get("", response_model=FolderContents)
async def list_home_content(user: gcu): # type: ignore
  return FolderContents(
    folders=await FolderPydanticSlim.from_queryset(Folder.filter(owner_id=user.id, parent_id=None)),
    documents=await DocumentPydanticSlim.from_queryset(Document.filter(owner_id=user.id, folder_id=None))
  )


@router.get("{folder_id}", response_model=FolderContents)
async def list_folder_content(folder_id: str, user: gcu): # type: ignore
  return FolderContents(
    folders=await FolderPydanticSlim.from_queryset(Folder.filter(owner_id=user.id, parent_id=folder_id)),
    documents=await DocumentPydanticSlim.from_queryset(Document.filter(owner_id=user.id, folder_id=folder_id))
  )
