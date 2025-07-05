"""
URL patterns for employee management
"""
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee URLs
    path('', views.employee_list, name='employee_list'),
    path('search-ajax/', views.employee_search_ajax, name='employee_search_ajax'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('create/', views.employee_create, name='employee_create'),
    path('<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('<int:pk>/deactivate/', views.employee_deactivate, name='employee_deactivate'),

    # Bulk Import URLs
    path('bulk-import/', views.bulk_employee_import, name='bulk_employee_import'),
    path('download-template/', views.download_employee_template, name='download_employee_template'),

    # Delete URLs
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('bulk-delete/', views.bulk_employee_delete, name='bulk_employee_delete'),

    # Salary Structure URLs
    path('<int:employee_pk>/salary/create/', views.salary_structure_create, name='salary_structure_create'),
    path('salary/<int:pk>/edit/', views.salary_structure_update, name='salary_structure_update'),
]
