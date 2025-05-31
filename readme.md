# Соцсеть для обмена фотографиями

REST API для соцсети, где можно публиковать посты с фото, комментировать и лайкать.

## Технологии

- Django 5.2.1
- Django REST Framework
- PostgreSQL
- Python 3.x

## Запуск проекта

1. Клонировать репозиторий:
   
   ```bash
   git clone https://github.com/Ip-59/spd-diplom.git
   cd spd-diplom/social_network
   ```

2. Создать виртуальное окружение:
   
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Установить зависимости:
   
   ```bash
   pip install -r requirements.txt
   ```

4. Настроить БД в `settings.py`

5. Сделать миграцию:
   
   ```bash
   python manage.py migrate
   ```

6. Создать суперпользователя:
   
   ```bash
   python manage.py createsuperuser
   ```

7. Запустить сервер:
   
   ```bash
   python manage.py runserver
   ```

8. Открыть в браузере:
   
   - API: http://127.0.0.1:8000/api/
   - Админка: http://127.0.0.1:8000/admin/

## Функциональность

### Пользователи могут:

- Регистрироваться и авторизоваться
- Создавать свои посты с текстом и фото
- Комментировать посты других
- Ставить лайки
- Редактировать (только) свои посты

### API endpoints:

- `GET /api/posts/` - список постов
- `POST /api/posts/` - создать пост
- `GET /api/posts/{id}/` - смотреть пост
- `POST /api/posts/{id}/like/` - лайкнуть
- `GET /api/comments/` - список комментов
- `POST /api/comments/` - создать коммент

## Авторизация

Для получения токена отправить POST-запрос на `/api/auth/token/`:

```json
{
    "username": "логин",
    "password": "пароль"
}
```

Использовать токен в заголовке:

```
Authorization: Token ваш_токен
```

## Структура проекта

```
social_network/
├── manage.py
├── requirements.txt
├── social_network/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── posts/
    ├── models.py
    ├── views.py
    ├── serializers.py
    └── urls.py
```

## Примечания

- Для загрузки изображений используется поле `new_images`
- Все посты могут смотреть все пользователи
- Создавать посты могут только авторизованные пользователи
- Редактировать пост может только автор
