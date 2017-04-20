import csv
import os
import sys
import numpy as np
from psychopy import core, visual, data, event
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def manual_events(recording_path, trial_duration, skiptime=0, events={}, bracket="", volume=1.,output_path="~/evaluation", non_redundant=True):
	"""Evaluate a behavioural recording.
	E.g. for forced swim test, press enter when the experiment starts and s/i to annotate the onset of the respective behaviours.
	!!! Add optional instructons screen !!!
	Mention e.g. that you need to press return to start the evaluation period.

	Parameters
	----------
	recording_path: str
		Path to the recording file.
	trial_duration: int
		Number of seconds the trial should last after pressing the evaluation start key.

	"""

	recording_path = os.path.expanduser(recording_path)
	csv_output_path = os.path.expanduser(output_path)+".csv"

	if os.path.exists(csv_output_path):
		print("There is already an evaluation file at "+csv_output_path+". Please specify a different output path.")
		return

	keylist = ['left','right','up','down','escape','return']
	experiment_keylist = events.keys()
	keylist.extend(experiment_keylist)

	#process brackets string
	x_y_brackets = bracket.split(",")
	if len(x_y_brackets) == 1 and x_y_brackets != [""]:
		x0, x1 = [float(i)/100 for i in x_y_brackets[0].split("-")]
		y0 = 0.
		y1 = 1.
	elif len(x_y_brackets) == 2:
		try:
			x0, x1 = [float(i)/100 for i in x_y_brackets[0].split("-")]
		except ValueError:
			x0 = 0.
			x1 = 1.
		try:
			y0, y1 = [float(i)/100 for i in x_y_brackets[1].split("-")]
		except ValueError:
			y0 = 0.
			y1 = 1.
	else:
		x0 = y0 = 0.
		x1 = y1 = 1.

	win = visual.Window(
		size=(2048, 1152), fullscr=True, screen=0,
		allowGUI=False, allowStencil=True,
		monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
		blendMode='avg', useFBO=True,
		units="norm",
		)

	# Initialize components for Routine "trial"
	trialClock = core.Clock()
	mov = visual.MovieStim3(
		win=win, name='mov',
		filename=recording_path,
		depth=0.0,
		volume=volume,
		units="norm",
		)

	#set full_movie dimensions based on aspect ratio (making one value from each operation float to ensure float division)
	if float(mov.size[0])/mov.size[1] < float(win.size[0])/win.size[1]:
		full_movie_y = 2.
		full_movie_x = 2*float(win.size[1])/win.size[0]/(float(mov.size[1])/mov.size[0])
	else:
		full_movie_y = 2*float(win.size[1])/win.size[0]/(float(mov.size[1])/mov.size[0])
		full_movie_x = 2.
	mov.size=(full_movie_x, full_movie_y)

	#position video so as to center bracket
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
	globalClock = core.Clock()  # to track the time since measurement started
	trialClock = core.Clock()  # to track the time since measurement started
	routineTimer = core.CountdownTimer()  # to track time remaining in the experiment

	# prepare evaluation variables
	mov.status = NOT_STARTED
	pre_evaluation = True
	outputWriter1 = csv.writer(open(csv_output_path,'w'), lineterminator ='\n')
	outputWriter1.writerow(["start","behaviour"])
	lastkey=""

	# Start evaluation
	globalClock.reset()
	while pre_evaluation or routineTimer.getTime() > 0:
		T = globalClock.getTime()
		t = trialClock.getTime()
		resp_key = event.getKeys(keyList=keylist)
		if pre_evaluation:
			if "return" in resp_key:
				trialClock.reset()
				routineTimer.reset()
				routineTimer.add(trial_duration)
				pre_evaluation=False
		elif resp_key:
			if resp_key[0] in experiment_keylist:
				if non_redundant and resp_key[0] == lastkey:
					pass
				else:
					tempArray = [t, events[resp_key[0]]]
					outputWriter1.writerow(tempArray)
					tempArray =[] # make sure no info persists
					lastkey = resp_key[0]

		#start movie and keep track of start time
		if t >= 0.0 and mov.status == NOT_STARTED:
			mov.tStart = T
			mov.setAutoDraw(True)

		if mov.status == FINISHED:
			break

		# check for quit (the Esc key)
		if "escape" in resp_key:
			outputWriter1.writerow([t, "QUIT"])
			core.quit()

		win.flip()


	outputWriter1.writerow([t, "END"])
	if mov.status != FINISHED:
		mov.setAutoDraw(False)
	win.close()
	return

# if __name__ == '__main__':
	# recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0078.mkv"
	# bracket = "34-66,"
	# bracket = ""
	# manual_events(recording_path,5,events={"s":"swimming","i":"immobility"}, bracket=bracket, volume=0.01)
