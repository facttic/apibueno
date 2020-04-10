from apscheduler.schedulers.blocking import BlockingScheduler
from scraping import Scraping
import logging

# logging.ERROR less verbose
LEVEL = logging.DEBUG
logging.basicConfig()
LOGGER = logging.getLogger('apscheduler').setLevel(LEVEL)

scheduler = BlockingScheduler()

# Here we can use days=1 instead
# A day from start
INTERVAL_MINUTES = 60 * 24

@scheduler.scheduled_job('interval', minutes=INTERVAL_MINUTES)
def tasks():
    print(f'This job is run every {INTERVAL_MINUTES} minutes.')
    Scraping()

print('Scheduler has started.........')
scheduler.start()
print('Scheduler has finished.........')
