from celery import shared_task
from .models import Student
import pandas as pd

@shared_task
def calculate_real_time_analytics():
    students = Student.objects.all().values()
    df = pd.DataFrame(students)

    if not df.empty:
        avg_studytime = df['study_time'].mean()
        avg_absences = df['absences'].mean()
        avg_failures = df['failures'].mean()
        avg_g3_predicted = df['g3_predicted'].mean()

        return {
            'avg_studytime': round(avg_studytime, 2),
            'avg_absences': round(avg_absences, 2),
            'avg_failures': round(avg_failures, 2),
            'avg_predicted_g3': round(avg_g3_predicted, 2)
        }
    return {}
