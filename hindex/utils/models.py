import uuid
from django.db import models


class BaseModel(models.Model):
    """Utility model that has an id primary key, a unique uuid, and created_at
    and updated_at datetime fields. Extend this model to inherit these fields.

    class MyModel(BaseModel):
        pass
    """
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
