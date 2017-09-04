from apscheduler.schedulers.blocking import BlockingScheduler
import content

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
	content.main()
    print('This job is run every three minutes.')

sched.start()