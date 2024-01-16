from django_cron import CronJobBase, Schedule
from .models import Worker

def reset():
    workers = Worker.objects.all()
    for worker in workers:
        if worker.status_w is not None:
            worker.status_w.set([])
        worker.observation_w = ""
        worker.save()
    pass