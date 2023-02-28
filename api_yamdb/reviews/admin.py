from django.contrib import admin

from .models import Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'genre', 'name', 'description', 'year',)
    search_fields = ('name', 'year')
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
