from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',) #Añadir los campos que se pueden leer

# Register your models here.
admin.site.register(Task, TaskAdmin)