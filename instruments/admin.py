from django.contrib import admin

from instruments.models import Instruments, Order

admin.site.register(Instruments)
admin.site.register(Order)
