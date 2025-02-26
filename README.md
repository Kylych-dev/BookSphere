```angular2html
[GET] /authors - список авторов     
[POST] /authors - создание автора   
[GET] /authors/{id} - детали автора 
[PUT] /authors/{id} - обновление автора 
[DELETE] /authors/{id} - удаление автора

[GET] /books - список книг с фильтрацией
[POST] /books - создание книги
[GET] /books/{id} - детали книги
[PUT] /books/{id} - обновление книги
[DELETE] /books/{id} - удаление книги

[GET] /favorites - список избранного
[POST] /favorites - добавить в избранное
[DELETE] /favorites/{id} - удалить из избранного
[DELETE] /favorites/clear - очистить избранное

[POST] /register - регистрация
[POST] /login - авторизация
[POST] /logout - выход
[POST] /token/refresh - обновление JWT-токена
```


# Инструкция по запуску проекта

Этот проект представляет собой API, реализованное с использованием Django и Django REST Framework, с использованием Docker для контейнеризации. В этом файле объясняется, как клонировать проект, настроить и запустить его локально или в Docker.

## Требования

- Docker
- Docker Compose
- Git
- Python 3.8 или выше (для разработки без Docker)

## Шаги по запуску

### 1. Клонировать репозиторий

Сначала клонируйте репозиторий с GitHub:

``` bash
git@github.com:Kylych-dev/BookSphere.git
cd ваша_папка 
```
2. Настроить виртуальное окружение (если вы не используете Docker)

Если вы хотите работать без Docker, создайте виртуальное окружение:

``` bash
python3 -m venv env
source env/bin/activate  # Для Windows используйте env\Scripts\activate
```

Установите зависимости:

``` bash
pip install -r requirements.txt
```

3. Настройка окружения
3.1 Переменные окружения

Создайте файл .env в корне проекта и добавьте следующие переменные окружения (или замените значениями вашего окружения):

```
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_BROKER_TRANSPORT_OPTIONS={"visibility_timeout": 3600}
CELERY_RESULT_BACKEND=redis://redis:6379/0

CELERY_ACCEPT_CONTENT=application/json
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=qwerty.qwerty@mail.ru
EMAIL_HOST_PASSWORD=qwerty

```

Примечание: Для генерации случайного значения SECRET_KEY, можно использовать команду:

python -c 'import secrets; print(secrets.token_urlsafe())'

3.2 Миграции базы данных

Для настройки базы данных выполните миграции:

``` bash
python manage.py migrate
```

4. Запуск проекта с Docker

Если вы хотите запустить проект с помощью Docker, выполните следующие шаги:
4.1 Сборка Docker-образа

    Убедитесь, что у вас установлен Docker и Docker Compose.
    Перейдите в корень проекта.
    Соберите и запустите контейнеры:

``` bash
docker-compose up --build
```

4.2 Запуск в Docker без сборки

Если образы уже собраны, можно просто запустить контейнеры:

docker-compose up

5. Доступ к приложению

После того как контейнеры будут запущены, вы сможете получить доступ к вашему API по следующему адресу:

    API: http://localhost:8000
    Админка Django (если настроена): http://localhost:8000/admin

6. Выполнение команд в контейнерах

Если вам нужно выполнить команды Django в контейнере, например, для создания суперпользователя, используйте:

``` bash
docker-compose exec web python manage.py createsuperuser
```


