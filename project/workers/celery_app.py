from __future__ import annotations

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("gifting")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    task_default_retry_delay=30,
    broker_transport_options={"visibility_timeout": 3600},
    task_routes={
        "workers.tasks.execute_gift_job": {"queue": "critical"},
        "workers.tasks.recovery_scan": {"queue": "recovery"},
    },
)
app.autodiscover_tasks(["workers"])
