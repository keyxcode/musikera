from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Composer)
admin.site.register(Epoch)
admin.site.register(Genre)
admin.site.register(Work)
admin.site.register(Like)