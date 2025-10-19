from core.models import Attendance, Class, Client
from .Repository import Repository

class AttendanceRepository(Repository):
    model = Attendance

    def add(self, date, class_id, client_id):
        # Отримуємо об'єкти за id
        class_instance = Class.objects.get(pk=class_id)
        client_instance = Client.objects.get(pk=client_id)

        # Створюємо запис Attendance
        attendance = self.model(
            date=date,
            class_field=class_instance,
            client=client_instance
        )
        attendance.save()
        return attendance