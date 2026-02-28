from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Resets and creates the specific requested users for the app'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Masters: deivid, wellington e paulo
        # Encarregados: Sandra e Alessandra
        # Operadores: Yasmin e Otilia
        # Senha: 123456
        
        user_data = [
            {'username': 'deivid', 'role': 'MASTER', 'first_name': 'Deivid'},
            {'username': 'wellington', 'role': 'MASTER', 'first_name': 'Wellington'},
            {'username': 'paulo', 'role': 'MASTER', 'first_name': 'Paulo'},
            {'username': 'sandra', 'role': 'ENCARREGADO', 'first_name': 'Sandra'},
            {'username': 'alessandra', 'role': 'ENCARREGADO', 'first_name': 'Alessandra'},
            {'username': 'yasmin', 'role': 'OPERADOR', 'first_name': 'Yasmin'},
            {'username': 'otilia', 'role': 'OPERADOR', 'first_name': 'Otilia'},
        ]
        
        for data in user_data:
            user, created = User.objects.get_or_create(username=data['username'])
            user.set_password('123456')
            user.role = data['role']
            user.first_name = data['first_name']
            user.save()
            
            action = "Criado" if created else "Atualizado"
            self.stdout.write(self.style.SUCCESS(f'{action} usuário: {user.username} (Role: {user.role})'))
        
        # Remove old test users if they exist
        for old_user in ['master', 'encarregado', 'auditoria']:
            try:
                u = User.objects.get(username=old_user)
                u.delete()
                self.stdout.write(self.style.WARNING(f'Usuário antigo {old_user} deletado.'))
            except User.DoesNotExist:
                pass
