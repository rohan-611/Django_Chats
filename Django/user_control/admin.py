from django.contrib import admin

from .models import CustomUser, JWT

# Register your models here.

admin.site.register(
    (
        CustomUser,
        JWT,
    )
)
