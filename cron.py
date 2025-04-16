from threading import Thread
import time
import random
import traceback

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

def helloWorld():
	print('Hello world', flush=True)

def runCronTasks():
	schedule(10, helloWorld)
