from django.contrib import admin
from django.db.models import Count

from .models import User, Team
from hindex.utils.admin import AlphabeticalDropDownFilter


@ admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'label',
        'user_count',
        'province',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_display_links = ('uuid',)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user_count = qs.annotate(user_count=Count('users', distinct=True))
        return user_count

    def user_count(self, obj):
        return obj.user_count
    user_count.admin_order_field = 'user_count'


@ admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_login',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        ('team__label', AlphabeticalDropDownFilter),
    )
    list_display_links = ('id',)
    raw_id_fields = ('groups', 'user_permissions', 'team')
    search_fields = ('id', 'username')
