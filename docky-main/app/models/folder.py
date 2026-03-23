from tortoise import fields, models

class Folder(models.Model):
  uuid = fields.UUIDField(pk=True)
  name = fields.CharField(100)
  created_at = fields.DatetimeField(auto_now_add=True)

  parent = fields.ForeignKeyField(
    "models.Folder",
    related_name="children",
    to_field='uuid',
    on_delete=fields.OnDelete.SET_NULL,
    null=True,
  )
  
  owner = fields.ForeignKeyField(
    "models.User",
    related_name="folders",
    to_field='id',
    on_delete=fields.OnDelete.RESTRICT,
  )

  class Meta:
    table = "folders"
