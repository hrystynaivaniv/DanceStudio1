from django.db import models

class DanceStyle(models.Model):
    dance_style_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dance_style'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'equipment'

    def __str__(self):
        return self.name


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    equipment = models.ManyToManyField(
        "Equipment",
        through="HallEquipment",
        related_name="halls"
    )

    class Meta:
        managed = False
        db_table = 'hall'

    def __str__(self):
        return self.name

class HallEquipment(models.Model):
    hall = models.ForeignKey(Hall, to_field="hall_id", on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, to_field="equipment_id", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = "hall_equipment"
        unique_together = ("hall", "equipment")


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'instructor'

    def __str__(self):
        return f"{self.name} {self.surname or ''}".strip()


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    visit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription'

    def __str__(self):
        return self.name or f"Subscription {self.subscription_id}"


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, to_field='subscription_id', on_delete=models.SET_NULL, blank=True, null=True, related_name='clients')

    class Meta:
        managed = False
        db_table = 'client'

    def __str__(self):
        return f"{self.name} {self.surname}"


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hall = models.ForeignKey(Hall, to_field='hall_id', on_delete=models.PROTECT, related_name='classes')
    dance_style = models.ForeignKey(DanceStyle, to_field='dance_style_id', on_delete=models.PROTECT, related_name='classes')
    instructor = models.ForeignKey(Instructor, to_field='instructor_id', on_delete=models.PROTECT, related_name='classes')

    class Meta:
        managed = False
        db_table = 'class'

    def __str__(self):
        return f"{self.dance_style.name} on {self.day_of_week}"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    date = models.DateField()
    class_field = models.ForeignKey(
        Class,
        to_field='class_id',
        db_column='class_id',  
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    client = models.ForeignKey(
        Client,
        to_field='client_id',
        db_column='client_id', 
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    class Meta:
        managed = False
        db_table = 'attendance'

    def __str__(self):
        return f"{self.client} attended {self.class_field} on {self.date}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    method = models.CharField(max_length=50)
    client = models.ForeignKey(Client, to_field='client_id', on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, to_field='subscription_id', on_delete=models.CASCADE, related_name='payments')

    class Meta:
        managed = False
        db_table = 'payment'

    def __str__(self):
        return f"{self.client} paid {self.amount} on {self.payment_date}"
