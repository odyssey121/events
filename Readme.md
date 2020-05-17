Пользователь создает событие (встреча, звонок и т.д.) с заголовком, содержанием и датой проведения. Пользователь должен иметь возможность совершать CRUD-операции над своими событиями. Искать по заголовку и фильтровать по дате (события за последние месяц, неделю, день)

Каждое событие должно иметь свой уникальный url-адрес.

За час до проведения события, сервис отправляет напоминание по e-mail автору.

#для тестовой развертки приложения выполнить:

    $ git clone https://github.com/odyssey121/events.git
    $ cd events
    $ make start
    $ make make_migrations
    $ make migrate
    $ make create_superuser
    $ make restart_django
    $ make collect_static
    
 - Django: http://localhost:8000
 - Adminer: http://localhost:8080
 - Nuxt.js: http://localhost:3000

## Автор

[Alexey Shirnin](https://github.com/odyssey121/)
