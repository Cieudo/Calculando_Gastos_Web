# models.py

from django.db import models

class Gasto(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'

