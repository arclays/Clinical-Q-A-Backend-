
# Register your models here.
from django.contrib import admin
from .models import DS_Questions, DS_Answers, DS_Views, CustomQuestion

admin.site.register(DS_Questions)
admin.site.register(DS_Answers)
admin.site.register(DS_Views)
admin.site.register(CustomQuestion)

