![example workflow](https://github.com/KondratevAD/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
[![codecov](https://codecov.io/gh/KondratevAD/foodgram-project-react/branch/master/graph/badge.svg?token=VTYOU2MVMS)](https://codecov.io/gh/KondratevAD/foodgram-project-react)
# Проект Foodgram-project-react

## Описание 
«Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект доступен по адресу: http://62.84.113.95
## Установка
Создайте в корневой директории файл с названием ".env" и поместите в него:
```
DB_NAME=имя_базы_данных
POSTGRES_USER=имя_пользователя 
POSTGRES_PASSWORD=пароль_пользователя
DB_HOST=хост
DB_PORT=порт
```
Создайте контейнеры и запустите их:
```bash
docker-compose up -d 
```

## После каждого обновления репозитория
* Проверка кода на соответствие стандарту PEP8 (flake8), pytest
* Сборка и доставка докер-образов на Docker Hub
* Деплой на сервер
* Отправка уведомления в Telegram

## Данные для входа
### Суперпользователь
```
Имя: admin
Email: admin@admin.ru
Password: admin
```
### Тестовый пользователь 1
```
Имя: Alex
Email: alex@bk.ru
Password: alex123456
```
### Тестовый пользователь 2
```
Имя: Sam
Email: sam@bk.ru
Password: sam123456
```