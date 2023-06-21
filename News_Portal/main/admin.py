from django.contrib import admin
# from .models import Post, Category, PostCategory, MyModel
from .models import Post, Category, PostCategory


# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)
from modeltranslation.admin import TranslationAdmin


# Register your models here.
 
# Регистрируем модели для перевода в админке
 
class CategoryAdmin(TranslationAdmin):
    model = Category
  

# class MyModelAdmin(TranslationAdmin):
#     model = MyModel
 

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)

# admin.site.register(MyModel)
