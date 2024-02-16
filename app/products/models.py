from django.db import models


class SGBDRProduct(models.Model):
    name = models.CharField(verbose_name="Name")
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Prix")

    class Meta:
        verbose_name = "SGBDR Product"
        verbose_name_plural = "SGBDR Products"
