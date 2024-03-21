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

    POSTGRES_NAME=<your_settings>
    POSTGRES_USER=<your_settings>
    POSTGRES_PASSWORD=<your_settings>
    POSTGRES_HOST=<your_settings>
    POSTGRES_PORT=<your_settings>
    CELERY_BROKER_URL=<your_settings>
    CELERY_RESULT_BACKEND=<your_settings>

### 4. Работа с Google API:  
1. Создайте проект Google Cloud  
https://developers.google.com/workspace/guides/create-project?hl=ru
2. Следуйте инструкции по настройке среды (необходимо включить API, настроить OAuth, авторизовать учетные данные для настольного приложения)  
https://developers.google.com/calendar/api/quickstart/python?hl=ru
3. Скачайте json file и переместите его в calendar_app/credentials/, так же переименуйте в credentials.json
4. Добавьте свой google email в список тестовых пользователей  
https://console.cloud.google.com/apis/credentials/consent

### 5. Получение token.json:
1. Настройте виртуальное окружение  
python3 -m venv venv  
source venv/bin/activate
pip3 install -r requirements.txt 
2. Запустите файл /calendar_app/credentials/oauth2.py
3. После открытия браузера, выполните аутентификацию со своего аккаунта Google
4. Сообщение об успешной операции: The authentication flow has completed. You may close this window.
5. Файл token.json появится в /calendar_app/credentials/
6. В /calendar_app/credentials/ должно быть 2 файла: credentials.json, который вы скачали со страницы настройки OAuth, и token.json, который появится после аутентификации в браузере

### 6. Соберите и запустите Docker контейнер, создайте суперпользователя:

    docker-compose build

    docker-compose up

    docker ps

    docker exec -it <ID_bank_api-django> python manage.py createsuperuser

### 7. Создание компании
Перейдите в админ панель и создайте компанию, доступные холлы(календари) и ивенты для холла подтянутся из Google Calendar в течение 120 секунд.

### 8. Функционал
Приложение переносит календари и ивенты в базу данных, при этом проверяет пересечения дат. Приложение работает согласно таймингу(120 секунд), который пользователь может поменять в настройках. По умолчанию синхронизируется только одна компания, что тоже можно поменять в настройках

### 9. Остановка Docker контейнера:

    docker-compose down