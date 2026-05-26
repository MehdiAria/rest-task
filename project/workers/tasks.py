from __future__ import annotations

from celery import shared_task
from django.db import transaction
from django.utils import timezone
from apps.gifting.models import PremiumGiftJob
from automation.engine import TelegramAutomationEngine


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=7, time_limit=900)
def execute_gift_job(self, job_id: str) -> None:
    with transaction.atomic():
        job = PremiumGiftJob.objects.select_for_update().get(id=job_id)
        if job.status == PremiumGiftJob.Status.SUCCESS:
            return
        job.status = PremiumGiftJob.Status.RUNNING
        job.save(update_fields=["status", "updated_at"])

    engine = TelegramAutomationEngine(worker_id=self.request.hostname or "unknown")
    result = engine.run_job(job)

    with transaction.atomic():
        job = PremiumGiftJob.objects.select_for_update().get(id=job_id)
        job.status = PremiumGiftJob.Status.SUCCESS if result else PremiumGiftJob.Status.RETRY
        job.retry_count += 0 if result else 1
        job.next_retry_at = None if result else timezone.now()
        job.save(update_fields=["status", "retry_count", "next_retry_at", "updated_at"])


@shared_task
def recovery_scan() -> int:
    stale = PremiumGiftJob.objects.filter(status=PremiumGiftJob.Status.RUNNING)
    count = stale.update(status=PremiumGiftJob.Status.RETRY)
    return count
