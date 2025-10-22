from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, date


class Contributor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=False)
    
    def __str__(self):
        return self.name
  
    class Meta:
        db_table = "contributor"



# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200,null=False)
    description = models.TextField(max_length=500)
    end_date = models.DateField()
    start = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)


    def clean(self):
        super().clean()
        if self.start and self.end_date:
            start_date = self.start.date()
            if self.end_date <= start_date:
                raise ValidationError('End date must be after the start date.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "task"


class Attendance(models.Model):
    date = models.DateField(default=date.today)
    is_available = models.BooleanField(default=False)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.contributor.name} - {self.date} - {'Available' if self.is_available else 'Unavailable'}"

    class Meta:
        db_table = "attendance"
        unique_together = ("contributor", "date")