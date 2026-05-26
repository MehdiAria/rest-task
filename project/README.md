# Telegram Premium Gifting Automation Platform

Enterprise-grade, recovery-first automation platform built with Django 5, DRF, PostgreSQL, Redis, Celery, OpenCV, PyAutoGUI, Xvfb, Telegram Desktop, Prometheus, and Grafana.

## Reliability Principles
- Stability over speed
- Recovery over performance
- Observability over minimalism
- Idempotent jobs and durable queues
- Safe automation with CV-based detection

## Architecture
- `apps/`: Django domain apps (core, gifting, monitoring)
- `automation/`: Telegram workflow engine + watchdogs + recovery orchestrator
- `cv/`: OpenCV detection primitives
- `workers/`: Celery app, task routing, retry policies
- `monitoring/`: Prometheus/Grafana configs
- `infrastructure/systemd/`: service units
- `docker/`: compose, Dockerfiles, bootstrap

See docs:
- `docs/deployment.md`
- `docs/vps_setup.md`
- `docs/xvfb_telegram.md`
- `docs/troubleshooting.md`
- `docs/disaster_recovery.md`
- `docs/scaling.md`
