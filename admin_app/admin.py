from django.contrib import admin
from admin_app.models import *
# Register your models here.
admin.site.register(User_management)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Team_management)
admin.site.register(Project)
admin.site.register(Report)
admin.site.register(Team_member)

