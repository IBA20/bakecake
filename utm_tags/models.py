from django.db import models
from django.utils import timezone


class UTMVisit(models.Model):
    source = models.CharField(
        max_length=100,
    )
    medium = models.CharField(
        max_length=100,
        blank=True,
    )
    campaign = models.CharField(
        max_length=100,
        blank=True,
    )
    term = models.CharField(
        max_length=100,
        blank=True,
    )
    content = models.CharField(
        max_length=100,
        blank=True,
    )
    timestamp = models.DateTimeField(
        default=timezone.now, help_text="When the event occurred."
    )

    class Meta:
        get_latest_by = ('timestamp',)

    def __str__(self):
        return f'UTM visit {self.id} from {self.source}'
