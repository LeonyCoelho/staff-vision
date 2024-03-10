from django.contrib import admin
from .models import Establishment, Sector, Sub_Sector, Position, Shift, Global_Settings, Status, Worker, CustomUser, Dashboard_Presets, Theme

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('establishment_name',)

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector_name',)

@admin.register(Sub_Sector)
class SubSectorAdmin(admin.ModelAdmin):
    list_display = ('subSector_name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name',)

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_name',)

@admin.register(Global_Settings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('sector_title', 'subSector_title')

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id_worker', 'name_w')

@admin.register(Dashboard_Presets)
class Dashboard_PresetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'preset_name')

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme_name')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ()
    ordering = ('name', )

    # def get_setores(self, obj):
    #     return ', '.join([sector.name for sector in obj.sector.all()])
    # get_setores.short_description = 'Setores'