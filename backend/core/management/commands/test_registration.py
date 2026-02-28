from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.test import Client
from core.models import Store, GasType
import json

class Command(BaseCommand):
    help = 'Testa a criacao de retiradas de gas para todos os usuarios'

    def handle(self, *args, **kwargs):
        from django.conf import settings
        if 'testserver' not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append('testserver')
            
        User = get_user_model()
        client = Client()
        
        users = [
            ('deivid', 'MASTER'),
            ('wellington', 'MASTER'),
            ('paulo', 'MASTER'),
            ('sandra', 'ENCARREGADO'),
            ('alessandra', 'ENCARREGADO'),
            ('yasmin', 'OPERADOR'),
            ('otilia', 'OPERADOR')
        ]
        
        stores = Store.objects.all()
        gas_types = GasType.objects.all()
        
        if not stores.exists() or not gas_types.exists():
            self.stdout.write(self.style.ERROR("Faltam lojas ou tipos de gas."))
            return
            
        gas_id = gas_types.first().id
        errors = 0
        successes = 0
        
        for username, role in users:
            self.stdout.write(f"\n--- Testando usuario: {username} ({role}) ---")
            
            # Login manual para pegar token
            response = client.post('/api/token/', {'username': username, 'password': '123456'}, content_type='application/json')
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Falha ao logar {username}"))
                errors += 1
                continue
                
            token = response.json()['access']
            headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
            
            for store in stores:
                payload = {
                    "store": store.id,
                    "pdv": "CX Teste",
                    "operator": username.capitalize(),
                    "retriever_name": "Testador Automático",
                    "gas_type": gas_id,
                    "quantity": 1
                }
                
                req = client.post('/api/withdrawals/', data=json.dumps(payload), content_type='application/json', **headers)
                if req.status_code == 201:
                    self.stdout.write(self.style.SUCCESS(f" [OK] Retirada na loja {store.name} criada."))
                    successes += 1
                else:
                    self.stdout.write(self.style.WARNING(f" [ERRO] Loja {store.name}: {req.status_code} - {req.content}"))
                    errors += 1
                    
        self.stdout.write(f"\nResumo: {successes} sucessos, {errors} erros.")
