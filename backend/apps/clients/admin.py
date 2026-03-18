from django.contrib import admin

from .models import Client, ClientAddress, Contact

admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(ClientAddress)
