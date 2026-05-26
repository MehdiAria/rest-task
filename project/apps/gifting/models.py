from __future__ import annotations

import uuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PremiumGiftJob(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        FAILED = "failed"
        RETRY = "retry"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT)
    telegram_username = models.CharField(max_length=64, db_index=True)
    duration_months = models.PositiveSmallIntegerField()
    message = models.CharField(max_length=256, blank=True)
    idempotency_key = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    retry_count = models.PositiveIntegerField(default=0)
    next_retry_at = models.DateTimeField(null=True, blank=True, db_index=True)


class AutomationSession(TimeStampedModel):
    worker_id = models.CharField(max_length=128, db_index=True)
    telegram_pid = models.IntegerField(null=True, blank=True)
    xvfb_display = models.CharField(max_length=16)
    is_healthy = models.BooleanField(default=True, db_index=True)
    last_heartbeat_at = models.DateTimeField(db_index=True)


class PaymentAttempt(TimeStampedModel):
    job = models.ForeignKey(PremiumGiftJob, on_delete=models.CASCADE, related_name="payment_attempts")
    successful = models.BooleanField(default=False, db_index=True)
    provider_reference = models.CharField(max_length=128, blank=True)
    diagnostic_payload = models.JSONField(default=dict)


class AutomationEvent(TimeStampedModel):
    job = models.ForeignKey(PremiumGiftJob, on_delete=models.CASCADE, related_name="events")
    session = models.ForeignKey(AutomationSession, on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=16, db_index=True)
    event_type = models.CharField(max_length=64, db_index=True)
    message = models.TextField()
    metadata = models.JSONField(default=dict)


class FailureLog(TimeStampedModel):
    job = models.ForeignKey(PremiumGiftJob, on_delete=models.CASCADE)
    exception_class = models.CharField(max_length=128)
    exception_message = models.TextField()
    traceback = models.TextField()
    is_recoverable = models.BooleanField(default=True)


class WorkerState(TimeStampedModel):
    worker_id = models.CharField(max_length=128, unique=True)
    queue = models.CharField(max_length=64)
    last_seen_at = models.DateTimeField(db_index=True)
    state = models.CharField(max_length=32, db_index=True)
    meta = models.JSONField(default=dict)
