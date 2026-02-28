from django.core.management.base import BaseCommand
from core.models import GasType, Stock

class Command(BaseCommand):
    help = 'Força a deleção dos gases extras e limpa seus estoques irreais.'

    def handle(self, *args, **kwargs):
        official_gases = ["Gás GLP Nacional", "Gás GLP Azul"]
        
        gases_to_delete = GasType.objects.exclude(name__in=official_gases)
        count = 0
        
        for gas in gases_to_delete:
            self.stdout.write(f"Deletando {gas.name}...")
            # Deletar estoques associados a esse gás
            stocks_deleted, _ = Stock.objects.filter(gas_type=gas).delete()
            self.stdout.write(f"   - {stocks_deleted} registros de estoque removidos.")
            
            gas.delete()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f"{count} tipos de gás extras deletados com sucesso!"))
