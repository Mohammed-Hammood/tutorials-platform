from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.unregister(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_login',  'date_joined', 'first_name', 'last_name']
    list_display_links = ['id', 'username', 'last_login',  'date_joined', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)