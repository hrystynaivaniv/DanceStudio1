from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import (
    DanceStyle, Equipment, Hall, HallEquipment, Instructor,
    Subscription, Client, Class, Attendance, Payment
)
from .serializers import (
    DanceStyleSerializer, EquipmentSerializer, HallSerializer, HallEquipmentSerializer,
    InstructorSerializer, SubscriptionSerializer, ClientSerializer, ClassSerializer,
    AttendanceSerializer, PaymentSerializer
)
from repositories.RepositoryManager import RepositoryManager

repo = RepositoryManager()

class DanceStyleViewSet(viewsets.ModelViewSet):
    repository = repo.dance_styles
    queryset = repository.get_all()
    serializer_class = DanceStyleSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    repository = repo.equipment
    queryset = repository.get_all()
    serializer_class = EquipmentSerializer


class HallViewSet(viewsets.ModelViewSet):
    repository = repo.halls
    queryset = repository.get_all()
    serializer_class = HallSerializer


class HallEquipmentViewSet(viewsets.ModelViewSet):
    repository = repo.hall_equipment
    queryset = repository.get_all()
    serializer_class = HallEquipmentSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    repository = repo.instructors
    queryset = repository.get_all()
    serializer_class = InstructorSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    repository = repo.subscriptions
    queryset = repository.get_all()
    serializer_class = SubscriptionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    repository = repo.clients
    queryset = repository.get_all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ClassViewSet(viewsets.ModelViewSet):
    repository = repo.classes
    queryset = repository.get_all()
    serializer_class = ClassSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    repository = repo.attendances
    queryset = repository.get_all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    repository = repo.payments
    queryset = repository.get_all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionReportView(APIView):
    def get(self, request):
        data = Subscription.objects.annotate(
            client_count=Count('clients')
        ).values('subscription_id', 'name', 'client_count')
        return Response(list(data))

from django.db.models import Sum

class HallEquipmentReportView(APIView):
    def get(self, request):
        data = HallEquipment.objects.values('hall__name').annotate(total_quantity=Sum('quantity'))
        return Response(list(data))
