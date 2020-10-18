from django import forms
from .models import Mails


# Форма для отображения писем не понадобилась
# class MailViewForm(forms.ModelForm):
#     class Meta:
#         model = Mails
#         fields = '__all__'


# Форма для создания письма
class MailSendForm(forms.Form):
    recipient = forms.EmailField(max_length=200, label='Кому (Email):')
    subject = forms.CharField(max_length=255, label='Тема:')
    defer = forms.IntegerField(min_value=0, max_value=900, label='Отослать через (сек):')
    send_date = forms.DateTimeField().hidden_widget  # Скрывает данное поле в шаблоне
    message = forms.CharField(widget=forms.Textarea, label='Сообщение:')

    # Переопределяем виджеты полей, добавляем Bootstrap класс 'form-control'
    recipient.widget.attrs.update({'class': 'form-control'})
    subject.widget.attrs.update({'class': 'form-control'})
    defer.widget.attrs.update({'class': 'form-control'})
    message.widget.attrs.update({'class': 'form-control'})

    def save(self):
        import datetime
        time_defer = self.cleaned_data['defer']
        new_mail = Mails.objects.create(
            recipient=self.cleaned_data['recipient'],
            subject=self.cleaned_data['subject'],
            defer=self.cleaned_data['defer'],
            send_date=datetime.datetime.now() + datetime.timedelta(seconds=time_defer),
            message=self.cleaned_data['message']
        )
        return new_mail

