from rest_framework import serializers
from .models import (
    DanceStyle, Equipment, Hall, HallEquipment, Instructor,
    Subscription, Client, Class, Attendance, Payment
)


class DanceStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceStyle
        fields = ('dance_style_id', 'name', 'description')
        read_only_fields = ('dance_style_id',)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('equipment_id', 'name')
        read_only_fields = ('equipment_id',)


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('hall_id', 'name', 'capacity')
        read_only_fields = ('hall_id',)


class HallEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallEquipment
        fields = ("id", "hall", "equipment", "quantity")


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('instructor_id', 'name', 'surname', 'phone')
        read_only_fields = ('instructor_id',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscription_id', 'name', 'price', 'visit')
        read_only_fields = ('subscription_id',)


class ClientSerializer(serializers.ModelSerializer):
    subscription = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), allow_null=True)

    class Meta:
        model = Client
        fields = ('client_id', 'name', 'surname', 'phone', 'email', 'subscription')
        read_only_fields = ('client_id',)


class ClassSerializer(serializers.ModelSerializer):
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())
    dance_style = serializers.PrimaryKeyRelatedField(queryset=DanceStyle.objects.all())
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())

    class Meta:
        model = Class
        fields = (
            'class_id', 'day_of_week', 'start_time', 'end_time',
            'hall', 'dance_style', 'instructor'
        )
        read_only_fields = ('class_id',)


class AttendanceSerializer(serializers.ModelSerializer):
    class_field = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Attendance
        fields = ('attendance_id', 'date', 'class_field', 'client')
        read_only_fields = ('attendance_id',)


class PaymentSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    subscription = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all())

    class Meta:
        model = Payment
        fields = (
            'payment_id', 'amount', 'payment_date', 'method',
            'client', 'subscription'
        )
        read_only_fields = ('payment_id',)


