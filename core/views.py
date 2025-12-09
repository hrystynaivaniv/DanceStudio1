from rest_framework import viewsets
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
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from django.db.models import Sum, Count, F, Max, Min, Avg
from django.db.models.functions import TruncMonth, TruncDate
from datetime import timedelta
from django.utils import timezone

import pandas as pd

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


class HallEquipmentViewSet(viewsets.ViewSet):
    repository = repo.hall_equipment

    def list(self, request):
        hall_id = request.query_params.get('hall_id')
        equipment_id = request.query_params.get('equipment_id')

        qs = HallEquipment.objects.all()
        if hall_id:
            qs = qs.filter(hall_id=int(hall_id))
        if equipment_id:
            qs = qs.filter(equipment_id=int(equipment_id))

        serializer = HallEquipmentSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(HallEquipment, pk=pk)
        serializer = HallEquipmentSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = HallEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            new_item = self.repository.add(**serializer.validated_data)
            return Response(HallEquipmentSerializer(new_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        hall_id = request.data.get('hall_id')
        equipment_id = request.data.get('equipment_id')

        if pk:
            rows = HallEquipment.objects.filter(pk=pk).update(**request.data)
        elif hall_id is not None and equipment_id is not None:
            rows = HallEquipment.objects.filter(hall_id=hall_id, equipment_id=equipment_id).update(**request.data)
        else:
            return Response({"error": "Provide pk or both hall_id and equipment_id in body"}, status=400)

        if rows == 0:
            return Response(status=404)
        return Response({"status": "Updated"}, status=200)

    partial_update = update

    def destroy(self, request, pk=None):
        hall_id = request.query_params.get('hall_id')
        equipment_id = request.query_params.get('equipment_id')

        try:
            hall_id = int(hall_id) if hall_id is not None else None
            equipment_id = int(equipment_id) if equipment_id is not None else None
        except ValueError:
            return Response({"error": "hall_id and equipment_id must be integers"}, status=400)

        if pk:
            deleted, _ = HallEquipment.objects.filter(pk=pk).delete()
        elif hall_id is not None and equipment_id is not None:
            deleted, _ = HallEquipment.objects.filter(hall_id=hall_id, equipment_id=equipment_id).delete()
        else:
            return Response({"error": "Provide pk or both hall_id and equipment_id as query params"}, status=400)

        if deleted == 0:
            return Response(status=404)
        return Response(status=204)


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


class AttendanceViewSet(viewsets.ViewSet):
    repository = repo.attendances

    def list(self, request):
        class_id = request.query_params.get('class_id')
        client_id = request.query_params.get('client_id')

        qs = Attendance.objects.all()
        if class_id:
            qs = qs.filter(class_field_id=int(class_id))
        if client_id:
            qs = qs.filter(client_id=int(client_id))

        serializer = AttendanceSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(Attendance, attendance_id=pk)
        serializer = AttendanceSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            new_item = self.repository.add(**serializer.validated_data)
            return Response(AttendanceSerializer(new_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        class_field = request.data.get('class_field_id')
        client = request.data.get('client_id')

        if pk:
            rows = Attendance.objects.filter(attendance_id=pk).update(**request.data)
        elif class_field is not None and client is not None:
            rows = Attendance.objects.filter(class_field_id=class_field, client_id=client).update(**request.data)
        else:
            return Response({"error": "Provide attendance_id or both class_field and client in body"}, status=400)

        if rows == 0:
            return Response(status=404)
        return Response({"status": "Updated"}, status=200)

    partial_update = update

    def destroy(self, request, pk=None):
        class_id = request.query_params.get('class_id')
        client_id = request.query_params.get('client_id')

        try:
            class_id = int(class_id) if class_id is not None else None
            client_id = int(client_id) if client_id is not None else None
        except ValueError:
            return Response({"error": "class_id and client_id must be integers"}, status=400)

        if pk:
            deleted, _ = Attendance.objects.filter(attendance_id=pk).delete()
        elif class_id is not None and client_id is not None:
            deleted, _ = Attendance.objects.filter(class_field_id=class_id, client_id=client_id).delete()
        else:
            return Response({"error": "Provide attendance_id or both class_id and client_id as query params"}, status=400)

        if deleted == 0:
            return Response(status=404)
        return Response(status=204)

class PaymentViewSet(viewsets.ModelViewSet):
    repository = repo.payments
    queryset = repository.get_all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]



class SubscriptionReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.subscriptions.get_subscriptions_with_client_count()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            revenue_attribute = df['client_count']
            stats = {
                'Medium': revenue_attribute.mean(),
                'Median': revenue_attribute.median(),
                'Min': revenue_attribute.min(),
                'Max': revenue_attribute.max(),
            }

        return Response({"data": df.to_dict('records'), "stats": stats})



class HallEquipmentReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.hall_equipment.get_total_equipment_by_hall()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            qty = df['total_quantity']
            stats = {
                'Medium': qty.mean(),
                'Median': qty.median(),
                'Min': qty.min(),
                'Max': qty.max(),
            }

        return Response({"data": df.to_dict('records'), "stats": stats})



class PaymentMethodRevenueReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.payments.get_revenue_by_method()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            revenue = df['total_revenue']
            stats = {
                'Medium': revenue.mean(),
                'Median': revenue.median(),
                'Min': revenue.min(),
                'Max': revenue.max(),
            }

        return Response({"data": df.to_dict('records'), "stats": stats})


class TopInstructorsByClassesReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.instructors.get_top_instructors()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            cnt = df['class_count']
            stats = {
                'Medium': cnt.mean(),
                'Median': cnt.median(),
                'Min': cnt.min(),
                'Max': cnt.max(),
            }

        return Response({"data": df.to_dict('records'), "stats": stats})



class MonthlyRevenueReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.payments.get_monthly_revenue()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            revenue = df['total_revenue']
            stats = {
                'Medium': revenue.mean(),
                'Median': revenue.median(),
                'Min': revenue.min(),
                'Max': revenue.max(),
            }

            df['month_year'] = df['month_year'].dt.strftime('%Y-%m')

        return Response({"data": df.to_dict('records'), "stats": stats})


class HallEfficiencyReportView(APIView):
    def get(self, request):
        repo = RepositoryManager()
        queryset = repo.halls.get_hall_efficiency()

        df = pd.DataFrame(list(queryset))

        stats = {}
        if not df.empty:
            eff = df['avg_attendees_per_class']
            stats = {
                'Medium': eff.mean(),
                'Median': eff.median(),
                'Min': eff.min(),
                'Max': eff.max(),
            }

            df['avg_attendees_per_class'] = df['avg_attendees_per_class'].round(2)

        return Response({"data": df.to_dict('records'), "stats": stats})
