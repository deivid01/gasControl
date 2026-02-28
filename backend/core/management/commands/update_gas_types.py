from django.core.management.base import BaseCommand
from core.models import GasType, Stock, Withdrawal

class Command(BaseCommand):
    help = 'Renomeia os dois tipos oficiais de gás para o sistema.'

    def handle(self, *args, **kwargs):
        official_gases = [
            "Gás GLP Nacional",
            "Gás GLP Azul"
        ]

        # 1. Obter ou Criar Tipos de Gás
        current_gases = list(GasType.objects.all().order_by('id'))
        
        for i, gas_name in enumerate(official_gases):
            if i < len(current_gases):
                gas = current_gases[i]
                gas.name = gas_name
                gas.save()
            else:
                GasType.objects.get_or_create(name=gas_name)

        # 2. Se houverem extras vazios, deletar. 
        # ATENCAO: Não podemos deletar se houver Withdrawals atrelados.
        if len(current_gases) > len(official_gases):
            for i in range(len(official_gases), len(current_gases)):
                gas = current_gases[i]
                if not Withdrawal.objects.filter(gas_type=gas).exists() and not Stock.objects.filter(gas_type=gas, quantity__gt=0).exists():
                    try:
                        gas.delete()
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Não foi possivel deletar o gas extra: {e}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Gás {gas.name} não foi deletado pois está em uso."))
        

        self.stdout.write(self.style.SUCCESS(f"Tipos de gás atualizados para os nomes oficiais!"))
