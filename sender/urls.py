from django.urls import path
from .views import MailCreate, mail_status


urlpatterns = [
    path('', MailCreate.as_view(), name='mail_create_url'),
    path('status/', mail_status, name='mail_status_url'),
]

