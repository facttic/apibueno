from apscheduler.schedulers.blocking import BlockingScheduler
from scraping import Scraping

scheduler = BlockingScheduler()

INTERVAL_MINUTES = 1


@scheduler.scheduled_job('interval', minutes=INTERVAL_MINUTES)
def tasks():
    print('This job is run every 1 minutes.')
    Scraping()

print('Scheduler has started.........')
scheduler.start()
print('Scheduler has finished.........')
