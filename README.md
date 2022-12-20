# API YaMDB
### Описание проекта.
Проект представляет собой сервис для блогеров, в котором каждый зарегистрированный пользователь может создавать посты и комментировать их, подписываться на понравившихся авторов.
Настоящий репозиторий - API для данного проекта.

##### Технологии.
В проекте использованы следующие технологии:
Python 3.7, Django 3.2, Django REST Framework, Simple JWT.
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mdkostrov/api_final_yatube.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение (для Windows):

```
python -m venv env
```

```
source venv/scripts/activate
```

Обновить установщик пакетов pip:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции (для Windows):

```
python manage.py migrate
```

Запустить проект (для Windows):

```
python manage.py runserver
```

### Документация
Документация с доступными для запросов эндпоинтами после запуска DEV-сервера проекта доступна по адресу:

```
http://127.0.0.1:8000/redoc/
```

### Об авторах:
Над проектом работали:
**Костров Михаил (тимлид)**
* [GitHub](https://github.com/mdkostrov/)
**Александр Морозов**
* [GitHub](https://github.com/notebad)
**Иван Наливайко**
* [GitHub](https://github.com/nemanick)
Студенты курса "Разработчик Python" (47 когорта).
