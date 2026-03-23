from tortoise import fields, models

class Document(models.Model):
  uuid = fields.UUIDField(pk=True)
  name = fields.CharField(100)
  size = fields.IntField()
  type = fields.CharField(64)
  uploaded_at = fields.DatetimeField(auto_now_add=True)
  thumbnail_blob = fields.BinaryField(null=True)

  folder = fields.ForeignKeyField(
    "models.Folder",
    related_name="documents",
    to_field='uuid',
    on_delete=fields.OnDelete.SET_NULL,
    null=True,
  )

  owner = fields.ForeignKeyField(
    "models.User",
    related_name="documents",
    to_field='id',
    on_delete=fields.OnDelete.RESTRICT,
  )

  class Meta:
    table = "documents"
