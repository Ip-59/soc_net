from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает токены для всех пользователей или для конкретного пользователя'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Имя пользователя для создания токена',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Создать токены для всех пользователей',
        )

    def handle(self, *args, **options):
        if options['username']:
            try:
                user = User.objects.get(username=options['username'])
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    print(f'Токен создан для пользователя {user.username}: {token.key}')
                else:
                    print(f'Токен уже существует для пользователя {user.username}: {token.key}')
            except User.DoesNotExist:
                print(f'Пользователь {options["username"]} не найден')
                
        elif options['all']:
            users = User.objects.all()
            for user in users:
                token, created = Token.objects.get_or_create(user=user)
                status = "создан" if created else "уже существует"
                print(f'Токен {status} для {user.username}: {token.key}')
                
        else:
            print('Укажите --username <имя> или --all для создания токенов')