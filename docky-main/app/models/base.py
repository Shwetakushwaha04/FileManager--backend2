from tortoise import fields, models

class BaseModel(models.Model):
  id = fields.IntField(pk=True)
  uid = fields.CharField(max_length=12, unique=True)

  class PydanticMeta:
    exclude = ['id']


class BaseUIDModel(models.Model):
  uid = fields.CharField(pk=True, max_length=12)


class BaseUUIDModel(models.Model):
  uuid = fields.UUIDField(pk=True)


class BaseUIDExtModel(BaseUIDModel):
  code = fields.CharField(max_length=64, unique=True, null=False)
  name = fields.CharField(max_length=128, unique=True, null=False)
  desc = fields.CharField(max_length=128, null=True)
  deleted = fields.BooleanField(default=False, null=False)
