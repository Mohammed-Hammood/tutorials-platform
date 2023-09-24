from django.contrib import admin
from .models import Product, ProductAccess, Lesson, LessonProgress


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'owner', 'created_at', 'updated_at']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user',  'duration', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'user',  'duration', 'created_at', 'updated_at']

class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ['id' , 'product', 'user']
    list_display_links = ['id' , 'product', 'user']

    

admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ProductAccess, ProductAccessAdmin)
admin.site.register(LessonProgress)