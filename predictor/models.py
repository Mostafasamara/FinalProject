from django.db import models

class StudentPerformance(models.Model):
    username = models.CharField(max_length=100)

    # ✅ Study & Lifestyle Factors
    Study_Hours_Per_Day = models.FloatField()
    Extracurricular_Hours_Per_Day = models.FloatField()
    Sleep_Hours_Per_Day = models.FloatField()
    Social_Hours_Per_Day = models.FloatField()
    Physical_Activity_Hours_Per_Day = models.FloatField()
    Stress_Level = models.IntegerField()  # Changed to Integer for categorical stress levels

    # ✅ Additional Performance Indicators
    StudyHoursPerWeek = models.FloatField(null=True, blank=True)
    AttendanceRate = models.FloatField(null=True, blank=True)
    Gender = models.CharField(max_length=50, null=True, blank=True)
    Major = models.CharField(max_length=255, null=True, blank=True)
    PartTimeJob = models.IntegerField(null=True, blank=True)  # Stored as 0 or 1
    ExtraCurricularActivities = models.IntegerField(null=True, blank=True)  # Stored as 0 or 1

    # ✅ Predicted GPA
    GPA = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - Predicted GPA: {self.GPA if self.GPA else 'N/A'}"
