from threading import Thread
import time
import random
import traceback
import logging
from syncbot.management.libraries import syncbot

logger = logging.getLogger(__name__)

def loop(interval, func):
	time.sleep(random.randint(5, 60)) # offset / jitter
	while True:
		try:
			func()
		except Exception:
			traceback.print_exc()
		time.sleep(interval)

def schedule(interval, func):
	f = lambda: loop(interval, func)
	t = Thread(target=f)
	t.daemon = True
	t.start()

def fetch():
	logger.info("Running syncbot.fetch...")
	syncbot.fetch()
	logger.info("Finished running syncbot.fetch.")

def synchronize():
	logger.info("Running syncbot.synchronize...")
	syncbot.synchronize()
	logger.info("Finished running syncbot.synchronize.")

def runCronTasks():
	#schedule(10, fetch)
	#schedule(10, synchronize)
