from rest_framework import serializers
from .models import PremiumGiftJob


class PremiumGiftJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumGiftJob
        fields = [
            "id",
            "telegram_username",
            "duration_months",
            "message",
            "idempotency_key",
            "status",
            "retry_count",
            "created_at",
        ]
        read_only_fields = ["status", "retry_count", "created_at"]
