import pytz
from django.db.models.query import EmptyQuerySet
from events.celery import app as celery_app
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Event
from django.core.mail import send_mass_mail


@celery_app.task
def notify():
    # получем события которые начнуться в течении часа
    events_for_notify = Event.objects.filter(notified=False, event_date__gt=datetime.now(tz=timezone.utc),
                                             event_date__lt=datetime.now(tz=timezone.utc) + timedelta(
                                                 seconds=3600)).select_related('author').values('id',
                                                                                                'title',
                                                                                                'author__email',
                                                                                                'event_date',
                                                                                                'description').all()
    # если ни чего нету ни чего и неделаем
    if not events_for_notify:
        return None

    notify_dict = {}
    # сортируем события по пользователю
    for e in events_for_notify:
        author_email = e['author__email']
        if author_email in notify_dict:
            notify_dict[author_email].append(e)
        else:
            notify_dict[author_email] = [e, ]

    messages = ()
    # создаем рассылки по каждому пользователю
    for (email, events) in notify_dict.items():
        subject = 'Ваши событие(я) начнутся в течении часа'
        _from = 'Event$@example.ru'
        message = '\n'.join([
            """{i} - событие: {title},\t описание: {desc},\t время: {event_date}""".format(
                i=index + 1,
                title=event['title'],
                desc=event['description'],
                event_date=event['event_date'].astimezone(pytz.timezone('Europe/Moscow')).strftime(
                    "%H:%M:%S %d-%m-%Y")
            )
            for index, event in enumerate(events)])
        messages = (*messages, (subject, message, _from, [email]))
    # рассылка
    send_mass_mail(messages, fail_silently=False)
    # обновление событий которые прошли рассылку
    Event.objects.filter(pk__in=[event['id'] for event in events_for_notify]).update(notified=True)
    # возвращаем сообщения которые были отправлены в бд
    return messages
        
