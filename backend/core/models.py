import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('MASTER', 'Master'),
        ('ENCARREGADO', 'Encarregado'),
        ('OPERADOR', 'Operador'),
        ('RELATORIO', 'Relatório / Auditoria')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OPERADOR')
    
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

class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='stocks', verbose_name="Loja")
    gas_type = models.ForeignKey(GasType, on_delete=models.PROTECT, related_name='stocks', verbose_name="Tipo de Gás")
    quantity = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store', 'gas_type'], name='unique_store_gas_stock')
        ]
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self):
        return f"{self.store.name} - {self.gas_type.name} (Saldo: {self.quantity})"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('ENTRADA', 'Entrada de Estoque (+)' ),
        ('SAIDA', 'Saída / Venda / Retirada (-)' )
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, related_name='movements', verbose_name="Estoque Afetado")
    quantity = models.IntegerField(verbose_name="Quantidade Movimentada")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, verbose_name="Tipo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Movimentado por")
    description = models.CharField(max_length=255, blank=True, verbose_name="Descrição (Opcional)")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_movement_type_display()}] Qtd: {self.quantity} - {self.stock} em {self.created_at.strftime('%d/%m/%Y %H:%M')}"
