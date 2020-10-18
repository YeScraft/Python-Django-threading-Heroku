from django.contrib import admin
from .models import Mails
# Register your models here.


@admin.register(Mails)
class MailAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'status')

