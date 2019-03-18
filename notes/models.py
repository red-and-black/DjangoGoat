from django.db import models

from common.models import TimeStampedModel


class Note(TimeStampedModel):
    sender = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='receiver'
    )
    content = models.TextField(max_length=255)

    class Meta:
        ordering = ['created']
