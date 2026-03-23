from fastapi import APIRouter, HTTPException, Response
from app.models.folder import Folder
from app.schemas import FolderPydanticSlim, FolderInPydantic
from app.lib import gcu

router = APIRouter()

@router.post("", response_class=Response, status_code=201)
async def create_folder(folder: FolderInPydantic, user: gcu): # type: ignore
    parent = await Folder.get_or_none(uuid=folder.parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent folder not found")
    elif parent.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to create a folder in this parent folder")
    
    obj = await Folder.create(**folder.dict(), owner_id=user.id)
    return Response(status_code=201)

@router.get("", response_model=list[FolderPydanticSlim])
async def list_folders(user: gcu): # type: ignore
  return await FolderPydanticSlim.from_queryset(Folder.filter(owner_id=user.id))
