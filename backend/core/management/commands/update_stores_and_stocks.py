from django.core.management.base import BaseCommand
from core.models import Store, GasType, Stock

class Command(BaseCommand):
    help = 'Renomeia as lojas padrão, deleta excedentes e cria estoques iniciais de 500 cotas.'

    def handle(self, *args, **kwargs):
        official_stores = [
            "Loja 1 Jardim América",
            "Loja 3 Boracéia",
            "Loja 4 Perimetral",
            "Loja 5 Borborema"
        ]

        # 1. Obter ou Criar Lojas
        current_stores = list(Store.objects.all().order_by('id'))
        
        for i, nome_loja in enumerate(official_stores):
            if i < len(current_stores):
                loja = current_stores[i]
                loja.name = nome_loja
                loja.save()
            else:
                Store.objects.get_or_create(name=nome_loja)

        # 2. Deletar extras se houver
        if len(current_stores) > len(official_stores):
            for i in range(len(official_stores), len(current_stores)):
                try:
                    current_stores[i].delete()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Não foi possivel deletar a loja extra: {e}"))
        
        # 3. Criar Estoques de 500 cotas para testes
        gastypes = GasType.objects.all()
        stores = Store.objects.all()
        
        for store in stores:
            for gas in gastypes:
                stock, created = Stock.objects.get_or_create(
                    store=store,
                    gas_type=gas,
                    defaults={'quantity': 500}
                )
                if not created and stock.quantity == 0:
                    stock.quantity = 500
                    stock.save()

        self.stdout.write(self.style.SUCCESS(f"Lojas renomeadas para os nomes oficiais e Estoques iniciais injetados com sucesso!"))
