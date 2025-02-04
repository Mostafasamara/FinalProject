from django.apps import AppConfig
import os
import logging

logger = logging.getLogger(__name__)

class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'

    def ready(self):
        """Train & save model on Django startup if needed."""
        try:
            # ✅ Import inside function to prevent circular imports
            from .ml_model import train_lifestyle_model, train_performance_model

            # ✅ Define Paths
            MODEL_PATH_LIFESTYLE = os.path.join(os.path.dirname(__file__), "student_lifestyle_model.pkl")
            MODEL_PATH_PERFORMANCE = os.path.join(os.path.dirname(__file__), "student_performance_model.pkl")

            # ✅ Train models only if missing
            if not os.path.exists(MODEL_PATH_LIFESTYLE) or not os.path.exists(MODEL_PATH_PERFORMANCE):
                logger.info("🚀 No trained models found! Training new models...")
                train_lifestyle_model()
                train_performance_model()
            else:
                logger.info("✅ Models are already trained. Skipping training.")

        except Exception as e:
            logger.error(f"❌ Model training error: {str(e)}")
