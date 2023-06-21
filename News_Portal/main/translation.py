# from .models import Category, MyModel
from .models import Category


# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions
 
 
# регистрируем наши модели для перевода
 
@register(Category)
class CategoryTranslationOptions(TranslationOptions):

    # указываем, какие именно поля надо переводить в виде кортежа
    fields = ('category_name', )
 
 
# @register(MyModel)
# class MyModelTranslationOptions(TranslationOptions):
#     fields = ('name', )
