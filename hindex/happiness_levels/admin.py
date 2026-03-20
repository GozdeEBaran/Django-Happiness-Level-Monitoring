from django.contrib import admin

from hindex.happiness_levels.models import HappinessLevel
from hindex.utils.admin import (AlphabeticalDropDownFilter,
                                AlphabeticalChoiceDropdownFilter)


@ admin.register(HappinessLevel)
class HappinessLevelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'level',
        'factor',
        'notes',
        'user',
        'user__team'
    )
    list_filter = (
        'created_at',
        'updated_at',
        ('level', AlphabeticalDropDownFilter),
        ('user__team__label', AlphabeticalDropDownFilter),
        ('factor', AlphabeticalChoiceDropdownFilter))

    list_display_links = ('id', 'uuid')
    date_hierarchy = 'created_at'
    search_fields = ('id', 'uuid', 'user__username')
    raw_id_fields = ('user',)

    def user__team(self, obj):
        return obj.user.team

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user__team")
