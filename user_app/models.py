from django.db import models
from django.contrib.auth.hashers import check_password,make_password
from admin_app.models import *
# Create your models here.
class Users(models.Model):
    ACTIVE_CHOICES = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
        ('Block', 'Block'),
    )
    users_id=models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=12)
    email = models.EmailField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=10,choices=ACTIVE_CHOICES,default='pending')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.firstname

class Personal_task(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('complete', 'Complete')
    ]
    personal_task_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class team_collaboration(models.Model):
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    comments=models.TextField(null=True)
    file = models.FileField(upload_to='attachments/',null=True)

class Report(models.Model):
    reports_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    personal_task_id = models.ForeignKey(Personal_task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    export_data = models.JSONField()

