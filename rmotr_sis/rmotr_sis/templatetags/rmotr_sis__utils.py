from django import template
from django.db import models

register = template.Library()


@register.filter
def admin_url(value, arg):
    """Extends and complements:
    https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#reversing-admin-urls
    """
    meta = None
    if hasattr(value, 'app_label') and hasattr(value, 'model_name'):
        meta = value
    elif isinstance(value, models.Model):
        meta = type(value)._meta
    else:
        raise AttributeError("Invalid argument. Value must be either "
                             "options containing app_label and model_name or "
                             "a model instance object.")
    return 'admin:%s_%s_%s' % (meta.app_label, meta.model_name, arg)
