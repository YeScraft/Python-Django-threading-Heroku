import threading
import time

from django.shortcuts import render
from django.conf import settings

from django.views.generic import View
from django.core.mail import send_mail

from .models import Mails
from .forms import MailSendForm


# Create your views here.


def mail_sender(new_mail):
    """Send defer mail"""

    time.sleep(new_mail.defer)  # Таймер ожидания

    subject = new_mail.subject
    recipient = new_mail.recipient
    message = new_mail.message
    status = send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    if status == 1:  # send_mail() возвращает 1 если письмо отправлено
        print('Меняем статус')
        new_mail.status = True  # Меняем статус на отправленное
        new_mail.save()
    return status


threads = []


class MailCreate(View):
    """Make response with MailSendForm"""

    def get(self, request):
        form = MailSendForm
        message = 'Эта форма создаёт и отправляет сообщения.'

        return render(request, 'sender/mail_create.html', context={'form': form, 'message': message})

    def post(self, request):
        mail = MailSendForm(request.POST)

        if mail.is_valid():
            new_mail = mail.save()  # Создаем новое письмо

            thread = threading.Thread(target=mail_sender, args=(new_mail,))  # Создаем новый поток
            threads.append(thread)  # Добавляем поток
            thread.start()  # Запускаем новый поток

            # Формируем сообщение, что письмо будет отправлено
            form = None
            message = 'Сообщение по адресу: {} будет отправлено: {}.'.format(new_mail.recipient,
                                                                             new_mail.send_date.strftime("%Y-%m-%d "
                                                                                                         "%H:%M:%S"))
            return render(request, 'sender/mail_create.html', context={'form': form, 'message': message})

        # Формируем сообщение если проскочили через валидатор формы
        else:
            message = 'У Вас ошибка при заполнении формы.'
            return render(request, 'sender/mail_create.html', context={'form': mail, 'message': message})


def mail_status(request):
    """Make response for /status"""

    # import operator
    import datetime

    mails = Mails.objects.all()

    in_process = []  # В работе
    last_ten = []  # Последние 10 добавленные к отправке (неотправленные)
    sended = []  # Отправленные
    not_sended = []  # Отправленные

    for mail in mails:
        if mail.status == True:
            sended.append(mail)

        # Без .replace(tzinfo=None) отказывался сравнивать форматы времени
        # Проверка, что письмо не было отправлено
        elif (mail.status == False) and \
                (mail.send_date.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None)):
            not_sended.append(mail)

        else:
            in_process.append(mail)

    # Формируем последнюю не отправленную десятку писем
    in_process.sort(key=lambda x: x.id, reverse=True)
    for i, mail in enumerate(in_process):
        if i < 10:
            last_ten.append(mail)

    # Другой метод сортировки
    # f = operator.attrgetter('send_date')
    # in_process = list(sorted(in_process, key=f))

    # Сортируем письма, что в процессе отправки по времени отправки
    in_process.sort(key=lambda x: x.send_date)

    return render(request, 'sender/mail_status.html', context={'in_process': in_process,
                                                                'sended': sended,
                                                                'not_sended': not_sended,
                                                                'last_ten': last_ten,
                                                                })
