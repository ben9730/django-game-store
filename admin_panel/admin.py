from django.contrib import admin
from .models import SalesReport

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sales', 'total_orders', 'most_sold_game')
    list_filter = ('date',)
    readonly_fields = ('date', 'total_sales', 'total_orders', 'most_sold_game')
