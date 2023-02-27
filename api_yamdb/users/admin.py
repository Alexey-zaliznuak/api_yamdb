from django.contrib import admin
from .models import User, Role


@admin.register(Role)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'can_edit_self_content',
        'can_edit_all_content',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(User)
