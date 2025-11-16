from core.models import Attendance, Class, Client
from .Repository import Repository

class AttendanceRepository(Repository):
    model = Attendance
