from django.db.models import Sum

from core.models import HallEquipment
from .Repository import Repository

class HallEquipmentRepository(Repository):
    model = HallEquipment

    def get_total_equipment_by_hall(self, equipment_id=None):
        queryset = self.model.objects

        if equipment_id and equipment_id != '':
            queryset = queryset.filter(equipment__equipment_id=equipment_id)

        return (
            queryset
            .values('hall__name')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
        )
