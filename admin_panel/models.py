from django.db import models


class SalesReport(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    most_sold_game = models.ForeignKey(
        'games.Game',
        on_delete=models.SET_NULL,
        null=True,
        related_name='most_sold_in_reports'
    )

    def __str__(self):
        return f"Sales Report - {self.date}"
