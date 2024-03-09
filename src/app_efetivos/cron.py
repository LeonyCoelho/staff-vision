from django_cron import CronJobBase, Schedule
from .models import Worker

def reset():
    workers = Worker.objects.all()
<<<<<<< HEAD
    print('STARTING WORKERS RESET')
    
    for worker in workers:
        worker.status_w.set([])  # Define a lista vazia
        worker.observation_w = ""  # Define a string vazia
        worker.save()

    print('WORKERS RESET COMPLETED')
=======
    for worker in workers:
        if worker.status_w is not None:
            worker.status_w.set([])
        worker.observation_w = ""
        worker.save()
>>>>>>> 30f4f925aadc4739c0673881ded798bd92a28b74
    pass