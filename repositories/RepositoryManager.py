from .ClientRepository import ClientRepository
from .ClassRepository import ClassRepository
from .HallEquipmentRepository import HallEquipmentRepository
from .HallRepository import HallRepository
from .EquipmentRepository import EquipmentRepository
from .InstructorRepository import InstructorRepository
from .DanceStyleRepository import DanceStyleRepository
from .SubscriptionRepository import SubscriptionRepository
from .AttendanceRepository import AttendanceRepository
from .PaymentRepository import PaymentRepository

class RepositoryManager:

    def __init__(self):
        self.clients = ClientRepository()
        self.classes = ClassRepository()
        self.halls = HallRepository()
        self.equipment = EquipmentRepository()
        self.hall_equipment = HallEquipmentRepository()
        self.instructors = InstructorRepository()
        self.dance_styles = DanceStyleRepository()
        self.subscriptions = SubscriptionRepository()
        self.attendances = AttendanceRepository()
        self.payments = PaymentRepository()
