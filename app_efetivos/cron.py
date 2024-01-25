from django_cron import CronJobBase, Schedule
from .models import Worker

def reset():
    workers = Worker.objects.all()
    print('STARTING WORKERS RESET')
    
    for worker in workers:
        worker.status_w.set([])  # Define a lista vazia
        worker.observation_w = ""  # Define a string vazia
        worker.save()

    print('WORKERS RESET COMPLETED')
    pass