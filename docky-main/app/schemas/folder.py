from pydantic import  ConfigDict
from tortoise.contrib.pydantic import pydantic_model_creator

from app.lib import alias_generator_in, alias_generator_out
from app.models import Folder


FolderPydantic = pydantic_model_creator(
  Folder, name="Folder", exclude=["owner.id", "owner.created_at"],
  model_config=ConfigDict(alias_generator=alias_generator_out)
)


FolderPydanticSlim = pydantic_model_creator(
  Folder, name="FolderSlim", exclude=["owner_id", "owner", "parent_id", "parent", "children", "documents"],
  model_config=ConfigDict(alias_generator=alias_generator_out)
)


FolderInPydantic = pydantic_model_creator(
  Folder, name="FolderIn", exclude_readonly=True, exclude=['owner_id'],
  model_config=ConfigDict(alias_generator=alias_generator_in)
)
