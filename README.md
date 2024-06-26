# Google Calendar

### Описание
Приложение для синхронизации календарей и ивентов из Google Calendars в базу данных.

### Требования для пользования приложением

Убедитесь, что Docker и Docker-Compose установлены на вашем ПК.

### 1. Склонируйте репозиторий:

    git clone https://github.com/IgChern/google_calendar

### 2. Перейдите по пути проекта:

    cd google_calendar

### 3. Создайте файл .env со своими собственными настройками:

    MYSQL_ENGINE=<your_settings>
    MYSQL_DATABASE=<your_settings>
    MYSQL_USER=<your_settings>
    MYSQL_PASSWORD=<your_settings>
    MYSQL_ROOT_PASSWORD=<your_settings>
    MYSQL_HOST=<your_settings>
    MYSQL_PORT=<your_settings>

### 4. Работа с Google API:  
1. Создайте проект Google Cloud  
https://developers.google.com/workspace/guides/create-project?hl=ru
2. Следуйте инструкции по настройке среды (необходимо включить API, настроить OAuth, авторизовать учетные данные для настольного приложения)  
https://developers.google.com/calendar/api/quickstart/python?hl=ru
3. Скачайте json file и переместите его в calendar_app/credentials/, так же переименуйте в credentials.json
4. Добавьте свой google email в список тестовых пользователей  
https://console.cloud.google.com/apis/credentials/consent

### 5. Получение token.json:
Настройте виртуальное окружение:  

    python3 -m venv venv 

    source venv/bin/activate   

    pip3 install -r requirements.txt

1. Запустите файл calendar_app/credentials/oauth2.py
2. После открытия браузера, выполните аутентификацию со своего аккаунта Google
3. Сообщение об успешной операции: The authentication flow has completed. You may close this window.
4. Файл token.json появится в /calendar_app/credentials/
5. В /calendar_app/credentials/ должно быть 2 файла: credentials.json, который вы скачали со страницы настройки OAuth, и token.json, который появится после аутентификации в браузере

### 6. Соберите и запустите Docker контейнер, создайте суперпользователя:

    docker-compose build

    docker-compose up

    docker ps

    docker exec -it <ID-django-app> python manage.py createsuperuser

### 7. Создание компании
Перейдите в админ панель и создайте компанию, доступные холлы(календари) и ивенты для холла подтянутся из Google Calendar в течение 120 секунд.

### 8. Функционал
Приложение переносит календари и ивенты в базу данных, при этом проверяет пересечения дат. Приложение работает согласно таймингу(120 секунд), который пользователь может поменять в настройках. По умолчанию синхронизируется только одна компания, что тоже можно поменять в настройках.
CELERYD_CONCURRENCY = 1 (Кол-во одновременно синхронизирующихся компаний)
IMPORT_TIME = 120 (Частота синхронизации (секунд))

### 9. Остановка Docker контейнера:

    docker-compose down