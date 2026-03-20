from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    ChoicesFieldListFilter
)


class AlphabeticalFilterMixin:
    def choices(self, changelist):
        choices = super().choices(changelist)
        sorted_choices = sorted(choices, key=lambda x: x['display'])
        # All should always appear at top
        all_choice = next(filter(lambda x: x['display'] == 'All', sorted_choices), None)
        sorted_choices.insert(0, sorted_choices.pop(sorted_choices.index(all_choice)))
        return sorted_choices


class AlphabeticalChoiceDropdownFilter(AlphabeticalFilterMixin, ChoicesFieldListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'


class AlphabeticalDropDownFilter(AlphabeticalFilterMixin, AllValuesFieldListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
