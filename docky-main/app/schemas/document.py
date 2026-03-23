from pydantic import  ConfigDict
from tortoise.contrib.pydantic import pydantic_model_creator

from app.lib import alias_generator_in, alias_generator_out
from app.models import Document


DocumentPydantic = pydantic_model_creator(
  Document, name="Document", exclude=["owner.id", "owner.created_at", "thumbnail_blob"],
  model_config=ConfigDict(alias_generator=alias_generator_out)
)


DocumentPydanticSlim = pydantic_model_creator(
  Document, name="DocumentSlim", exclude=["owner_id", "owner", "folder_id", "folder", "thumbnail_blob"],
  model_config=ConfigDict(alias_generator=alias_generator_out)
)


DocumentInPydantic = pydantic_model_creator(
  Document, name="DocumentIn", exclude_readonly=True, exclude=['owner_id', 'thumbnail_blob'],
  model_config=ConfigDict(alias_generator=alias_generator_in)
)
