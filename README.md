# Что это
Web-UI для Docker. Используя:
- Django REST Framework
- Vue.js
- SDK Docker for Python

# Запуск
1. Запуск на хосте
   1. `python -m pip install pipenv`
   2. `pipenv install`
   3. `pipenv shell`
   4. `python manage.py makemigrations`
   5. `python manage.py migrate`
      1. `python manage.py runserver 0.0.0.0 8000` - стандартный запуск django
      2. `python manage.py runasync 0.0.0.0:8000` - многопоточный запуск через uvicorn, статика не будет отображаться.
2. Запуск в docker
   1. `pipenv lock -r > requirements.txt` - сохранить актульные требования python
   2. Настроить `Dockerfile`/`docker-compose.yml`
   3. `docker-compose -f docker-compose.yml up --force-recreate -d`
   4. `docker-compose -f docker-compose.yml exec django python /app/manage.py migrate`


## Примеры Конфигов
- Unix socket
```
Base url: unix://var/run/docker.sock
```

