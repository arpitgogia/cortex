from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from .models import Source, AllUrl


@admin.register(Source, AllUrl)
class SourceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = ('state',)
    readonly_fields = ('state',)
