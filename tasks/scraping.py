from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina'
INTERVAL_MINUTES = 1


@scheduler.scheduled_job('interval', minutes=INTERVAL_MINUTES)
def scrap():
    print('This job is run every 1 minutes.')
    print(f'scraping data from ${URL}........')


print('Scheduler has started.........')
scheduler.start()
print('Scheduler has finished.........')
