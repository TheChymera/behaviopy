import csv
import os
from psychopy import core, visual, data, event
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def evaluate_db():
	return

def evaluate(recording_path, trial_duration, events={},bracket="", volume=1.):
	"""Evaluate a behavioural recording.

	Parameters
	----------
	recording_path: str
		Path to the recording file.
	trial_duration: int
		Number of seconds the trial should last after pressing the evaluation start key.

	"""

	recording_path = os.path.expanduser(recording_path)

	keylist = ['left','right','up','down','escape','return']
	experiment_keylist = events.keys()
	keylist.extend(experiment_keylist)

	#set up evaluation data handling
	# trials = data.TrialHandler([{"a":"a"}], 1)
	# trials.data.addDataType('event')  # this will help store things with the stimuli
	# trials.data.addDataType('time')  # add as many types as you like

	#process brackets string
	x_y_brackets = bracket.split(",")
	if len(x_y_brackets) == 1:
		x0, x1 = [float(i) for i in x_y_brackets[0].split("-")]
		y0 = 0.
		y1 = 1.
	elif len(x_y_brackets) == 2:
		try:
			x0, x1 = [float(i) for i in x_y_brackets[0].split("-")]
		except ValueError:
			x0 = 0.
			x1 = 1.
		try:
			y0, y1 = [float(i) for i in x_y_brackets[1].split("-")]
		except ValueError:
			y0 = 0.
			y1 = 1.

	win = visual.Window(
		size=(2048, 1152), fullscr=True, screen=0,
		allowGUI=False, allowStencil=True,
		monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
		blendMode='avg', useFBO=True,
		units="norm",
		)

	# Initialize components for Routine "trial"
	trialClock = core.Clock()
	mov = visual.MovieStim(
		win=win, name='mov',
		filename=recording_path,
		depth=0.0,
		volume=volume,
		units="norm",
		size=2,
		)

	#position video in order to center bracket
	mov_xsize, mov_ysize = mov.size
	movsection_xpos = (x0+x1)/2.
	movsection_ypos = (y0+y1)/2.
	mov_xpos = mov_xsize*(1./2.-movsection_xpos)
	mov_ypos = mov_ysize*(1./2.-movsection_ypos)
	mov.pos = (mov_xpos,mov_ypos)

	#set aperture to bracket
	movsection_xsize = x1-x0
	movsection_ysize = y1-y0
	aperture_x = movsection_xsize*mov_xsize
	aperture_y = movsection_ysize*mov_ysize
	aperture = visual.Aperture(win, size=(aperture_x,aperture_y), pos=(0, 0), ori=0, nVert=120, shape='square', inverted=False, name=None, autoLog=None)

	# Create some handy timers
	globalClock = core.Clock()  # to track the time since experiment started
	routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

	# ------Prepare to start Routine "trial"-------
	t = 0
	trialClock.reset()  # clock
	frameN = -1
	mov.status = NOT_STARTED

	pre_evaluation = True
	responses = []
	# -------Start Routine "trial"-------
	while pre_evaluation or routineTimer.getTime() > 0:
		# get current time
		t = trialClock.getTime()
		resp_key = event.getKeys(keyList=keylist)
		if pre_evaluation:
			if "return" in resp_key:
				routineTimer.reset()  # clock
				routineTimer.add(trial_duration)
				pre_evaluation=False
		elif resp_key:
			if resp_key[0] in experiment_keylist:
				tempArray = [t, events[resp_key[0]]]
				responses.append(tempArray)
				# trials.addData('event', resp_key[0])  # add the data to our set
				# trials.addData('time', t)
				# trials.data.add('event', resp_key[0])  # add the data to our set
				# trials.data.add('time', t)


		#start movie and keep track of start time
		if t >= 0.0 and mov.status == NOT_STARTED:
			mov.tStart = t
			mov.setAutoDraw(True)

		if mov.status == FINISHED:
			break

		# check for quit (the Esc key)
		if "escape" in resp_key:
			core.quit()

		win.flip()

	print responses
	outputWriter1 = csv.writer(open('/home/chymera/src/behaviopy/behaviopy/fileName.csv','w'), lineterminator ='\n')
	for i in range(0, len(responses)):
		outputWriter1.writerow(responses[i])
	# trials.printAsText(stimOut=['a'],dataOut=['event', 't'])
	# a = trials.saveAsWideText("testDataWide.txt")
	# print a
	win.close()

if __name__ == '__main__':
	recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0037.mkv"
	recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0038.mkv"
	recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0039.mkv"
	bracket = "0-.24,"
	bracket = ".24-.42,"
	bracket = ".42-.59,"
	bracket = ".59-.77,"
	bracket = ".77-1,"
	bracket = ".4-.58,"
	bracket = ".2-.4,"
	bracket = ".58-.75,"
	evaluate(recording_path,5,events={"s":"swimming","f":"floating"}, bracket=bracket, volume=0)
