[![Django-app workflow](https://github.com/Vladimir-spb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Vladimir-spb/yamdb_final/actions/workflows/yamdb_workflown.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

# API YAMDB
## Оглавление
=======
1. [Описание проекта](https://github.com/Vladimir-spb/api_yamdb#описание-проекта)
2. [Как развернуть](https://github.com/Vladimir-spb/api_yamdb#как-развернуть)
3. [Работа с API](https://github.com/Vladimir-spb/api_yamdb#работа-с-api)
    1. [Доступные запросы](https://github.com/Vladimir-spb/api_yamdb#доступные-запросы)
    2. [Аутентификация](https://github.com/Vladimir-spb/api_yamdb#аутентификация) 
    3. [Примеры запросов и ответов](https://github.com/Vladimir-spb/api_yamdb#примеры-запросов-и-ответов) 
4. [Об авторах](https://github.com/Vladimir-spb/api_yamdb#об-авторах)

## Описание проекта
Проект _**YaMDb**_ собирает **отзывы** пользователей на **произведения**. Сами произведения в _**YaMDb**_ не хранятся, здесь нельзя посмотреть фильм или послушать музыку.  
  
**Произведения** делятся на **категории**: «Книги», «Фильмы», «Музыка». Список **категорий** может быть расширен администратором.  
Произведению может быть присвоен **жанр** из списка предустановленных. Новые **жанры** может создавать только администратор.  
Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению **оценку** в диапазоне от **1** до **10** (целое число); из пользовательских **оценок** формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.  
  
В проекте реализован _**API**_-**сервис** для аутентификации пользователей и работы со всеми вышеперечисленными ресурсами. Подробнее в разделе [примеров запросов и ответов](https://github.com/Vladimir-spb/api_yamdb#примеры-запросов-и-ответов). Аутентификация пользователей реализована по стандарту _**JWT**_.  

## Работа с API
### Доступные запросы
| Запрос | Эндпоинт | Метод |
|--------|:---------|-------|
| Регистрация нового пользователя |`.../api/v1/auth/signup/`| POST |
| Получение JWT-токена |`.../api/v1/auth/token/`| POST |
| Получение списка всех категорий |`.../api/v1/categories/`| GET |
| Добавление новой категории |`.../api/v1/categories/`| POST |
| Удаление категории |`.../api/v1/categories/{slug}/`| DELETE |
| Получение списка всех жанров |`.../api/v1/genres/`| GET |
| Добавление жанра |`.../api/v1/genres/`| POST |
| Удаление жанра |`.../api/v1/genres/{slug}/`| DELETE |
| Получение списка всех произведений |`.../api/v1/titles/`| GET |
| Добавление произведения |`.../api/v1/titles/`| POST |
| Получение информации о произведении |`.../api/v1/titles/{title_id}/`| GET |
| Частичное обновление информации о произведении |`.../api/v1/titles/{title_id}/`| PATCH |
| Удаление произведения |`.../api/v1/titles/{title_id}/`| DELETE |
| Получение списка всех отзывов |`.../api/v1/titles/{title_id}/reviews/`| GET |
| Добавление нового отзыва |`.../api/v1/titles/{title_id}/reviews/`| POST |
| Получение отзыва по id |`.../api/v1/titles/{title_id}/reviews/{review_id}/`| GET |
| Частичное обновление отзыва по id |`.../api/v1/titles/{title_id}/reviews/{review_id}/`| PATCH |
| Удаление отзыва по id |`.../api/v1/titles/{title_id}/reviews/{review_id}/`| DELETE |
| Получение списка всех комментариев к отзыву |`.../api/v1/titles/{title_id}/reviews/{review_id}/comments/`| GET |
| Добавление комментария к отзыву |`.../api/v1/titles/{title_id}/reviews/{review_id}/comments/`| POST |
| Получение комментария к отзыву |`.../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`| GET |
| Частичное обновление комментария к отзыву |`.../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`| PATCH |
| Удаление комментария к отзыву |`.../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`| DELETE |
| Получение списка всех пользователей |`.../api/v1/users/`| GET |
| Добавление пользователя |`.../api/v1/users/`| POST |
| Получение пользователя по username |`.../api/v1/users/{username}/`| GET |
| Изменение данных пользователя по username |`.../api/v1/users/{username}/`| PATCH |
| Удаление пользователя по username |`.../api/v1/users/{username}/`| DELETE |
| Получение данных своей учетной записи |`.../api/v1/users/me/`| GET |
| Изменение данных своей учетной записи |`.../api/v1/users/me/`| PATCH |
### Аутентификация
#### Алгоритм регистрации пользователей
1. Пользователь отправляет _**POST**_-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `.../api/v1/auth/signup/`.  
> Пример запроса:  
> _**POST .../api/v1/auth/signup/**_  
> ```JSON
> {
>   "email": "string",
>   "username": "string"
> }
> ```
> Пример ответа (200):
> ```JSON
> {
>   "email": "string",
>   "username": "string"
> }
> ```
2. YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет _**POST**_-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (_JWT_-токен).
> Пример запроса:  
> _**POST .../api/v1/auth/token/**_  
> ```JSON
> {
>   "username": "string",
>   "confirmation_code": "string"
> }
> ```
> Пример ответа (200):
> ```JSON
> {
>   "token": "string"
> }
> ```
4. При желании пользователь отправляет _**PATCH**_-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.
> Пример запроса:  
> _**POST .../api/v1/users/me/**_  
> ```JSON
> {
>   "username": "string",
>   "email": "user@example.com",
>   "first_name": "string",
>   "last_name": "string",
>   "bio": "string"
> }
> ```
> Пример ответа (200):
> ```JSON
> {
>   "username": "string",
>   "email": "user@example.com",
>   "first_name": "string",
>   "last_name": "string",
>   "bio": "string"
>   "role": "user"
> }
> ```
#### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладет правами администратора (`admin`)  
### Примеры запросов и ответов
После того, как проект [развёрнут и запущен](https:github.com/Vladimir-spb/api_yamdb#как-развернуть), документацию по API можно найти на эндпоинте `.../api/v1/redoc/`.
## Об авторах
Над проектом работали [Владимир Коршак](https://github.com/Vladimir-spb), [Антон Шлёнов](https://github.com/CodeDemonTony) и [Даниил Паутов](https://github.com/TomatoInOil), студенты Яндекс.Практикума. Это была замечательная командная работа!


# CI/CD для проекта API YAMDB

## Технологический стек
[![Django-app workflow](https://github.com/Vladimir-spb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Vladimir-spb/yamdb_final/actions/workflows/yamdb_workflown.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)


## Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовка для запуска workflow
Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
```
Запустите автотесты:
```
pytest
```
Отредактируйте файл `nginx/default.conf` и в строке `server_name` впишите IP виртуальной машины (сервера).  
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер:

Зайдите в репозиторий на локальной машине и отправьте файлы на сервер.
Можно сделать 2умя способами, первый склонировав репозиторий, переместив нужные файлы командой mv
после чего удалить остаток 
```
rm -rf hw05_final
```
Или 2ой вариант:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
ALLOWED_HOSTS - список разрешённых адресов
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
```

## Как запустить проект на сервере:


Установите Docker и Docker-compose:
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте корректность установки Docker-compose:
```
sudo  docker-compose --version
```
Создайте папку `nginx`:
```
mkdir nginx
```
### После успешного деплоя:
Соберите статические файлы (статику):
```
docker-compose exec web python manage.py collectstatic --no-input
```
Примените миграции:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser

```
или
```
docker-compose exec web python manage.py loaddata fixtures.json
```

## Развёрнутый проект
http://62.84.120.240/api/v1/
http://62.84.120.240/admin/
http://62.84.120.240/redoc/