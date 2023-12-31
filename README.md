l# Тестовое задание APPTRIX tinder_site

Сайт для знакомств на API Django Rest Framework

## Адрес сайта

http://51.250.19.113/

## Существующие эндпоинты

### Регистрация нового пользователя

```
POST /api/clients/create

```

Обязательные поля для заполнения:

* first_name
* last_name
* email
* password
* gender
* avatar (обработка при регистрации - наложение водяного знака)
* longitude - 55.15827406029935 для челябинска
* latitude - 61.38865235475735 для челябинска

### Получение токена авторизации

```
POST /api/auth/jwt/create
```

Необходимо передавать токен с каждым запросом с заголовком `Authorization` со значением `Bearer {token}`.

### Эндпоинт оценивания участником другого участника

```
POST /api/clients/{id}/match
```

В случае взаимной симпатии оба пользователя получают письмо с текстом "Вы понравились {имя}".

### Получение списка всех пользователей 

```
GET /api/list
```

Возвращаются следующие данные пользователей (с пагинацией - 5 пользователей на странице):

* first_name
* last_name
* gender
* avatar
* longitude
* latitude

Доступна фильтрация по `first_name`, `last_name`, `gender` и дистанции до участников.
Для фильтрации по дистанции используйте следующие query parameters в URL:

* distance_min=x - не ближе, чем x километров
* distance_max=y - не далее, чем y километров

Пример получения списка всех Сашей в радиусе 5 км:

```
GET /api/list?first_name=Саша&distance_max=5
```