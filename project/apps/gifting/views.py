from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PremiumGiftJob
from .serializers import PremiumGiftJobSerializer
from workers.tasks import execute_gift_job


class PremiumGiftJobViewSet(viewsets.ModelViewSet):
    serializer_class = PremiumGiftJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PremiumGiftJob.objects.filter(requested_by=self.request.user).order_by("-created_at")

    @transaction.atomic
    def perform_create(self, serializer):
        job = serializer.save(requested_by=self.request.user)
        execute_gift_job.delay(str(job.id))
