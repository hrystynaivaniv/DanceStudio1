from core.models import Hall, Equipment
from .Repository import Repository

class HallRepository(Repository):
    model = Hall

    def add_equipment(self, hall_id, equipment_ids):
        hall = self.get_by_id(hall_id)
        if hall:
            equipments = Equipment.objects.filter(pk__in=equipment_ids)
            hall.equipment.add(*equipments)
            return hall
        return None

    def remove_equipment(self, hall_id, equipment_ids):
        hall = self.get_by_id(hall_id)
        if hall:
            equipments = Equipment.objects.filter(pk__in=equipment_ids)
            hall.equipment.remove(*equipments)
            return hall
        return None
