from django.contrib import admin
from .models import (
    PAYETaxBand, TaxRelief, NSSFRate, SHIFRate,
    AffordableHousingLevyRate
)


@admin.register(PAYETaxBand)
class PAYETaxBandAdmin(admin.ModelAdmin):
    list_display = ['lower_limit', 'upper_limit', 'tax_rate', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    ordering = ['lower_limit']


@admin.register(TaxRelief)
class TaxReliefAdmin(admin.ModelAdmin):
    list_display = ['relief_type', 'amount', 'rate', 'maximum_amount', 'effective_date', 'is_active']
    list_filter = ['relief_type', 'is_active', 'effective_date']
    ordering = ['relief_type', '-effective_date']


@admin.register(NSSFRate)
class NSSFRateAdmin(admin.ModelAdmin):
    list_display = ['tier', 'lower_limit', 'upper_limit', 'contribution_rate', 'effective_date', 'is_active']
    list_filter = ['tier', 'is_active', 'effective_date']
    ordering = ['tier', 'lower_limit']


@admin.register(SHIFRate)
class SHIFRateAdmin(admin.ModelAdmin):
    list_display = ['contribution_rate', 'minimum_contribution', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    ordering = ['-effective_date']


@admin.register(AffordableHousingLevyRate)
class AffordableHousingLevyRateAdmin(admin.ModelAdmin):
    list_display = ['employee_rate', 'employer_rate', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    ordering = ['-effective_date']
