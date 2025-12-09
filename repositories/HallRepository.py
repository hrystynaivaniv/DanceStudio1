from django.db.models import Count, F

from core.models import Hall, Equipment
from .Repository import Repository

class HallRepository(Repository):
    model = Hall

    def get_hall_efficiency(self, limit = 5, dance_style_id=None):
        queryset = self.model.objects.all()

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 5

        if dance_style_id and dance_style_id != '':
            queryset = queryset.filter(classes__dance_style__dance_style_id=dance_style_id)

        results = (
            queryset
            .annotate(
                total_attendees=Count('classes__attendances', distinct=True),
                total_classes=Count('classes', distinct=True)
            )
            .filter(total_classes__gt=0)
            .annotate(
                avg_attendees_per_class=F('total_attendees') / F('total_classes')
            )
            .values('name', 'avg_attendees_per_class')
            .order_by('-avg_attendees_per_class')[:limit]
        )
        return results