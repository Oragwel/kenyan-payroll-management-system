"""
URL patterns for payroll processing
"""
from django.urls import path
from . import views

app_name = 'payroll_processing'

urlpatterns = [
    path('calculator/', views.payroll_calculator, name='payroll_calculator'),
    path('tax-calculator/', views.tax_calculator, name='tax_calculator'),
    path('calculate-ajax/', views.calculate_payroll_ajax, name='calculate_payroll_ajax'),
    path('employee/<int:employee_id>/', views.employee_payroll_detail, name='employee_payroll_detail'),
    path('payslip/<int:payslip_id>/', views.view_payslip, name='view_payslip'),
    path('payslip/generate/<int:employee_id>/', views.generate_payslip, name='generate_payslip'),
    path('reports/', views.payroll_reports, name='payroll_reports'),
    path('generate/', views.payroll_generation, name='payroll_generation'),
    path('periods/', views.payroll_periods, name='payroll_periods'),
    path('periods/<int:period_id>/', views.payroll_period_detail, name='payroll_period_detail'),
    path('periods/<int:period_id>/download/', views.download_period_payslips, name='download_period_payslips'),
    path('periods/<int:period_id>/delete/', views.payroll_period_delete, name='payroll_period_delete'),
    path('periods/bulk-delete/', views.bulk_payroll_period_delete, name='bulk_payroll_period_delete'),

    # Export URLs - Obfuscated
    path('data-export/summary/', views.export_payroll_summary, name='export_payroll_summary'),
    path('data-export/tax-analysis/', views.export_tax_report, name='export_tax_report'),
    path('data-export/compliance/', views.export_statutory_returns, name='export_statutory_returns'),
    path('data-export/personnel/', views.export_employee_list, name='export_employee_list'),
]
