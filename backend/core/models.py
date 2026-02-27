from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('MASTER', 'Master'),
        ('ENCARREGADO', 'Encarregado'),
        ('RELATORIO', 'Relatório / Auditoria')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ENCARREGADO')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Loja")
    # Loja 1 Jardim América, Loja 3 Boracéia, Loja 4 Perimetral, loja 5 Borborema
    
    def __str__(self):
        return self.name

class GasType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Gás")
    # Nacional, Azul
    
    def __str__(self):
        return self.name

class Withdrawal(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, verbose_name="Loja")
    pdv = models.CharField(max_length=50, verbose_name="PDV")
    operator = models.CharField(max_length=100, verbose_name="Operador do Caixa")
    retriever_name = models.CharField(max_length=100, verbose_name="Nome de quem retirou")
    gas_type = models.ForeignKey(GasType, on_delete=models.PROTECT, verbose_name="Tipo de Gás")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora da Retirada")
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Registrado por")
    
    # Rastreamento de Auditoria
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.quantity}x {self.gas_type.name} - {self.store.name} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
