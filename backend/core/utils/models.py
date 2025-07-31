import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


def hex_uuid():
    return uuid.uuid4().hex


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            return self.get(public_id=public_id)
        except ObjectDoesNotExist:
            return None


class AbstractModel(models.Model):
    public_id = models.UUIDField(
        default=hex_uuid,
        db_index=True,
        unique=True,
        editable=False,
        verbose_name="Public ID",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated",
    )

    objects = AbstractManager()

    class Meta:
        abstract = True
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
