from django.contrib import admin

from .models import Title, Category, Genre, Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('title', 'text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('review', 'text',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name', 'description', 'year',)
    search_fields = ('name', 'description')
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Genre)
