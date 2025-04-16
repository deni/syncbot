from threading import Thread
import time
import random

def loop(interval, func):
	time.sleep(random.randint(5, 60)) # offset / jitter
	while True:
		func()
		time.sleep(interval)

def schedule(interval, func):
	f = lambda: loop(interval, func)
	t = Thread(target=f)
	t.daemon = True
	t.start()

def helloWorld():
	print('Hello world')

def runCronTasks():
	schedule(10, helloWorld)
