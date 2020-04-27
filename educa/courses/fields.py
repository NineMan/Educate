from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_field=None, *args, **kwargs):
        self.for_fields = for_field
        super(OrderField, self).__init__(*args, **kwargs)

