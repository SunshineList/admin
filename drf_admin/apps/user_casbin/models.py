from django.db import models


# Create your models here.

class CasbinRule(models.Model):
    ptype = models.CharField(max_length=255)
    sub = models.CharField(max_length=255)
    obj = models.CharField(max_length=255, blank=True)
    action = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "casbin规则"
        verbose_name_plural = verbose_name
