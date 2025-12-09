from django.db.models import Count

from core.models import Subscription
from .Repository import Repository

class SubscriptionRepository(Repository):
    model = Subscription

    def get_subscriptions_with_client_count(self, subscription_id=None):
        queryset = self.model.objects

        if subscription_id:
            queryset = queryset.filter(subscription_id=subscription_id)

        return (
            queryset
            .annotate(client_count=Count('clients'))
            .values('subscription_id', 'name', 'client_count')
        )
