from datetime import timedelta, datetime

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from core.models import Payment
from .Repository import Repository

class PaymentRepository(Repository):
    model = Payment

    def get_revenue_by_method(self):
        return (
            self.model.objects
            .values('method')
            .annotate(total_revenue=Sum('amount'))
            .order_by('-total_revenue')
        )

    def get_monthly_revenue(self, min_date=None, max_date=None): 
        queryset = self.model.objects

        if not min_date and not max_date:
            one_year_ago = timezone.now().date() - timedelta(days=365)
            queryset = queryset.filter(payment_date__gte=one_year_ago)

        if min_date:
            try:
                min_date_obj = datetime.strptime(min_date, '%Y-%m-%d').date()
                queryset = queryset.filter(payment_date__gte=min_date_obj)
            except ValueError:
                pass

        if max_date:
            try:
                max_date_obj = datetime.strptime(max_date, '%Y-%m-%d').date()
                queryset = queryset.filter(payment_date__lte=max_date_obj)
            except ValueError:
                pass

        return (
            queryset
            .annotate(month_year=TruncMonth('payment_date'))
            .values('month_year')
            .annotate(total_revenue=Sum('amount'))
            .order_by('month_year')
        )