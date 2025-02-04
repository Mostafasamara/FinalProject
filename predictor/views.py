from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudentPerformance
import logging

# ✅ Correctly Import the Entire Module
from predictor import ml_model

logger = logging.getLogger(__name__)

class PredictStudentPerformance(APIView):
    """API to predict GPA based on student performance."""

    def post(self, request):
        try:
            # ✅ Extract data from request
            data = request.data
            logger.info(f"📩 Received data: {data}")

            # ✅ Validate input fields
            required_fields = [
                "username",
                "Study_Hours_Per_Day",
                "Extracurricular_Hours_Per_Day",
                "Sleep_Hours_Per_Day",
                "Social_Hours_Per_Day",
                "Physical_Activity_Hours_Per_Day",
                "Stress_Level",
                "StudyHoursPerWeek",
                "AttendanceRate",
                "Gender",
                "Major",
                "PartTimeJob",
                "ExtraCurricularActivities"
            ]

            # ✅ Check for missing fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return Response(
                    {"error": f"Missing fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Convert categorical fields ('Yes'/'No') into numeric values (1/0)
            binary_fields = ["PartTimeJob", "ExtraCurricularActivities"]
            for field in binary_fields:
                if data[field] in ["Yes", "No"]:
                    data[field] = 1 if data[field] == "Yes" else 0

            # ✅ Prepare data for model
            lifestyle_data = {key: data[key] for key in [
                "Study_Hours_Per_Day",
                "Extracurricular_Hours_Per_Day",
                "Sleep_Hours_Per_Day",
                "Social_Hours_Per_Day",
                "Physical_Activity_Hours_Per_Day",
                "Stress_Level"
            ]}

            performance_data = {key: data[key] for key in [
                "StudyHoursPerWeek",
                "AttendanceRate",
                "Gender",
                "Major",
                "PartTimeJob",
                "ExtraCurricularActivities"
            ]}

            # ✅ Predict GPA using the correctly imported module
            predicted_gpa = ml_model.predict_student_performance(lifestyle_data, performance_data)
            logger.info(f"📊 Predicted GPA: {predicted_gpa}")

            # ✅ Save Prediction to Database
            student_perf = StudentPerformance.objects.create(
                username=data["username"],
                GPA=predicted_gpa,
                Study_Hours_Per_Day=data["Study_Hours_Per_Day"],
                Extracurricular_Hours_Per_Day=data["Extracurricular_Hours_Per_Day"],
                Sleep_Hours_Per_Day=data["Sleep_Hours_Per_Day"],
                Social_Hours_Per_Day=data["Social_Hours_Per_Day"],
                Physical_Activity_Hours_Per_Day=data["Physical_Activity_Hours_Per_Day"],
                Stress_Level=data["Stress_Level"],
                StudyHoursPerWeek=data["StudyHoursPerWeek"],
                AttendanceRate=data["AttendanceRate"],
                Gender=data["Gender"],
                Major=data["Major"],
                PartTimeJob=data["PartTimeJob"],
                ExtraCurricularActivities=data["ExtraCurricularActivities"]
            )

            return Response({"GPA": round(predicted_gpa, 2)}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"❌ API Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
