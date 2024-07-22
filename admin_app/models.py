from django.db import models
from user_app.models import *
# Create your models here.
class User_management(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    user_permissions=models.TextField()

    def __str__(self):
        return self.user_id

class Team(models.Model):
    ACTIVE_CHOICES = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
    )
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.CharField(max_length=10, choices=ACTIVE_CHOICES,default='pending')


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('done','Done'),
        ('not started','Not started'),
        ('skipped','Skipped'),
    )
    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=100)
    description = models.TextField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title

class Team_management(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=100)


    def __str__(self):
        return self.team_name

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('not started', 'Not started'),
    )
    project_id=models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    export_data = models.JSONField()




