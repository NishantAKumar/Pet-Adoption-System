from django.contrib import admin
from .models import User, Transaction, Request, Queries
# Register your models here.

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Request)
admin.site.register(Queries)