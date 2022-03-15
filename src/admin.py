from django.contrib import admin
from .models import User, Report, Official, Notification, Contact



admin.site.register(User)
admin.site.register(Report)
admin.site.register(Official)
admin.site.register(Notification)
admin.site.register(Contact)
