from django.db import models


# Create your models here.


class Trim(models.Model):
    link = models.CharField(max_length=512, verbose_name="Original Link")
    code = models.CharField(max_length=16, verbose_name="Hashed Code", blank=True)
    noc = models.PositiveIntegerField(verbose_name="Number of click", default=0, blank=True, null=True)

    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "Link: %s" % self.link


class ClickInfo(models.Model):
    link = models.ForeignKey(Trim, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link.link