from django.db import models


# Create your models here.


class Trim(models.Model):
    link = models.URLField(verbose_name="Original Link")
    code = models.CharField(max_length=16, verbose_name="Hashed Code", blank=True)

    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return "Link: %s" % self.link
