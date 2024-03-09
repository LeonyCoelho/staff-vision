from django.contrib import admin
from django.urls import path
from app_efetivos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),
    path('view_by_sector/<int:id>/', views.view_by_sector, name='view_by_sector'),
    path('view_by_status/<int:id>/', views.view_by_status, name='view_by_status'),

    path('login/', views.login, name='login'),
    path('logout_view/', views.logout_view, name='logout_view'),

    path('settings/',views.settings, name='settings'),
    path('apply_defauts', views.apply_defauts, name='apply_defauts'),
    path('welcome', views.welcome, name='welcome'),
    path('welcome2', views.welcome2, name='welcome2'),
    path('welcome3', views.welcome3, name='welcome3'),
    path('welcome4', views.welcome4, name='welcome4'),
    path('create_default_settings/', views.create_default_settings, name='create_default_settings'),

    path('users/',views.users, name='users'),
    path('users/new_user/',views.new_user, name='new_user'),
    path('users/edit_user/<int:id>/',views.edit_user, name='edit_user'),
    path('users/delete_user/<int:id>/', views.delete_user, name='delete_user'),
    
    path('new_worker/',views.new_worker, name='new_worker'),
    path('update_worker/',views.update_worker, name='update_worker'),    
    path('remove_worker_status/<int:worker_id>/', views.remove_worker_status, name='remove_worker_status'),
    path('adjust_worker/',views.adjust_worker, name='adjust_worker'),
    path('edit_worker/<int:id_worker>/',views.edit_worker, name='edit_worker'),


    path('change_settings', views.change_settings, name='change_settings'),
    path('change_settings2', views.change_settings2, name='change_settings2'),
    path('change_logo', views.change_logo, name='change_logo'),
    path('remove_logo', views.remove_logo, name='remove_logo'),
    path('change_bg', views.change_bg, name='change_bg'),
    path('remove_bg', views.remove_bg, name='remove_bg'),
    path('export-workers-to-excel/', views.export_workers_to_excel, name='export_workers_to_excel'),
    path('import-workers-from-excel/', views.import_workers_from_excel, name='import_workers_from_excel'),
    path('remove_all_workers/', views.remove_all_workers, name='remove_all_workers'),
    path('get_import_progress/', views.get_import_progress, name='get_import_progress'),


    path('dashboard_settings', views.dashboard_settings, name='dashboard_settings'),
    path('dashboard_settings/delete_selected_presets/', views.delete_selected_presets, name='delete_selected_presets'),
    path('dashboard_settings/edit_preset/<int:id>/', views.edit_preset, name='edit_preset'),
    path('dashboard_settings/edit_layout/<int:id>/', views.edit_layout, name='edit_layout'),
    path('dashboard_settings/update_positions/<int:id>/', views.update_positions, name='update_positions'),
    path('dashboard_settings/auto_update_positions/<int:id>/', views.auto_update_positions, name='auto_update_positions'),
    path('dashboard_settings/reset_update_positions/<int:id>/', views.reset_update_positions, name='reset_update_positions'),
    path('dashboard_settings/update_position/<int:id>/', views.update_position, name='update_position'),
    path('dashboard_settings/update_sector_width/<int:sector_id>/<int:new_width>/', views.update_sector_width, name='update_sector_width'),
    path('dashboard_settings/update_header_width/<int:preset_id>/<int:new_width>/', views.update_header_width, name='update_header_width'),

    
    path('delete_selected_establishments/', views.delete_selected_establishments, name='delete_selected_establishments'),
    path('rename_establishment/', views.rename_establishment, name='rename_establishment'),

    path('delete_selected_sector/', views.delete_selected_sector, name='delete_selected_sectors'),
    path('rename_sector/', views.rename_sector, name='rename_sector'),

    path('delete_selected_sub_sector/', views.delete_selected_sub_sector, name='delete_selected_sub_sectors'),
    path('rename_sub_sector/', views.rename_sub_sector, name='rename_sub_sector'),

    path('delete_selected_position/', views.delete_selected_position, name='delete_selected_positions'),
    path('rename_position/', views.rename_position, name='rename_position'),

    path('delete_selected_shift/', views.delete_selected_shift, name='delete_selected_shifts'),
    path('rename_shift/', views.rename_shift, name='rename_shift'),
    
    path('delete_selected_status/', views.delete_selected_status, name='delete_selected_statuss'),
    path('rename_status/', views.rename_status, name='rename_status'),
    path('change_status_color/', views.change_status_color, name='change_status_color'),

    path('reset_all/', views.reset_all, name='reset_all'),
    path('history/', views.history, name='history'),
    path('worker_history/<int:worker_id>/', views.worker_history, name='worker_history'),
]



if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
