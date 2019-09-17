from django.contrib import admin


from .models import Superhero, Power, Photo


# Register your models here.


admin.site.register(Superhero)
admin.site.register(Power)
admin.site.register(Photo)

